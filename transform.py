#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Transformations matrix usefull tools."""
import numpy as np
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
import math


class Transform(object):
    """Transformation matrices utilities class."""

    @staticmethod
    def inverse(tr):
        """Return the inverse of the given transformation matrix."""
        # tr = np.asarray(tr)
        # print(tr, np.shape(tr))
        # Extraction matrice rotation
        r = tr[0:3:1, 0:3:1]
        # Exraction du vecteur de poerhfmsqkaq
        t = tr[0:3:1, 3:4:1]
        # Transposé de r
        rt = np.transpose(r)

        t2 = -rt.dot(t)

        res = np.ndarray((4, 4))
        res[0:3:1, 0:3:1] = rt
        res[0:3:1, 3:4:1] = t2
        res[3:4:1, :] = [0, 0, 0, 1]
        return res

    @staticmethod
    def flat_matrix_to_44(matrix):
        """Conversion de matrice 1d vers 2d."""
        mat = np.ndarray(shape=(4, 4))
        for k, v in enumerate(matrix):
            ligne = k / 4
            colone = k % 4
            mat[ligne][colone] = v
        mat[3][:] = 0
        mat[3][3] = 1
        return mat

    @staticmethod
    def error(t1, t2):
        u"""Return euclidian distance and distance (angle) between rotations.

        distance : euclidian
        angle : θ=arccos(trR−1)/2
        """
        dist = np.linalg.norm(np.asarray(t1)[0:3, 3:4] -
                              np.asarray(t2)[0:3, 3:4])
        R = t1[0:3, 0:3].dot(np.transpose(t2[0:3, 0:3]))
        theta = np.arccos((min(np.trace(R), 3) - 1) / 2)
        return dist, theta

    @staticmethod
    def to_quaternion(t):
        """Return quaternion computed from transformation matrix."""
        q = np.array([1.0, 0, 0, 0])
        trace = np.trace(t[0:3, 0:3])
        if trace > 0:
            s = math.sqrt(trace + 1.0) * 2
            q[0] = 0.25 * s
            q[1] = (t[2, 1] - t[1, 2]) / s
            q[2] = (t[0, 2] - t[2, 0]) / s
            q[3] = (t[1, 0] - t[0, 1]) / s
        elif t[0, 0] > t[1, 1] and t[0, 0] > t[2, 2]:
            s = math.sqrt(1.0 + t[0, 0] - t[1, 1] - t[2, 2]) * 2
            q[0] = (t[2, 1] - t[1, 2]) / s
            q[1] = 0.25 * s
            q[2] = (t[0, 1] + t[1, 0]) / s
            q[3] = (t[0, 2] + t[2, 0]) / s
        elif t[1, 1] > t[2, 2]:
            s = math.sqrt(1.0 + t[1, 1] - t[0, 0] - t[2, 2]) * 2
            q[0] = (t[0, 2] - t[2, 0]) / s
            q[1] = (t[0, 1] + t[1, 0]) / s
            q[2] = 0.25 * s
            q[3] = (t[1, 2] + t[2, 1]) / s
        else:
            s = math.sqrt(1.0 + t[2, 2] - t[0, 0] - t[1, 1]) * 2
            q[0] = (t[1, 0] - t[0, 1]) / s
            q[1] = (t[0, 2] + t[2, 0]) / s
            q[2] = (t[1, 2] + t[2, 1]) / s
            q[3] = 0.25 * s
        return q
    # def to_quaternion(t):
    #     """Return quaternion computed from transformation matrix."""
    #     q = np.array([1, 0, 0, 0])
    #     print(t)
    #     q[0] = math.sqrt(max(0, 1 + t[0, 0] + t[1, 1] + t[2, 2])) / 2
    #     q[1] = math.sqrt(max(0, 1 + t[0, 0] - t[1, 1] - t[2, 2])) / 2
    #     q[2] = math.sqrt(max(0, 1 - t[0, 0] + t[1, 1] - t[2, 2])) / 2
    #     q[3] = math.sqrt(max(0, 1 - t[0, 0] - t[1, 1] + t[2, 2])) / 2
    #     print(q)
    #     q[1] = math.copysign(q[1], t[2, 1] - t[1, 2])
    #     q[2] = math.copysign(q[2], t[0, 2] - t[2, 0])
    #     q[3] = math.copysign(q[3], t[1, 0] - t[0, 1])
    #     print(q)
    #     return q

    @staticmethod
    def to_Pose(t):
        """Return geometry_msgs/Pose conversion of transformation matrix."""
        quat = Transform.to_quaternion(t)
        pose = Pose()
        # print(t)
        # print(quat)
        pose.orientation.w = quat[0]
        pose.orientation.x = quat[1]
        pose.orientation.y = quat[2]
        pose.orientation.z = quat[3]
        pose.position.x = t[0, 3]
        pose.position.y = t[1, 3]
        pose.position.z = t[2, 3]
        return pose

    @staticmethod
    def to_PoseStamped(t, crt_time, frame='map'):
        """Return geometry_msgs/Pose conversion of transformation matrix."""
        trans = np.asarray(t)
        poseStamped = PoseStamped()
        poseStamped.pose = Transform.to_Pose(trans)
        poseStamped.header.frame_id = frame
        poseStamped.header.stamp = crt_time
        print(poseStamped.pose)
        return poseStamped
