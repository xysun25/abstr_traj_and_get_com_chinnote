# -*- coding:utf-8 -*-
# 作者 ：路飞太郎
# 时间 : 2022/11/07
# 简述: 中文且详细版本，从LAMMPS的输出轨迹文件（.xyz）中提取想要的帧数，并输出阴离子和阳离子坐标

import numpy as np
import pandas as pd
import MDAnalysis as mda
import os, re

## 第一部分： 从LAMMPS 的输出轨迹文件（.xyz）中提取想要的轨迹帧数

# 一个处理轨迹文件的类，两个功能/方法：1.读文件 2.提取轨迹文件想要的帧数
class ReadTraj():
    # 构造器方法，设置初始值
    def __init__(self,trajfile):
        self.trajfile = trajfile

    # 读轨迹文件的方法
    def read_traj(self):
        frames = 0
        timesteps = []
        if os.path.exists(self.trajfile):
            f1 = open(self.trajfile,"r")   # 如果轨迹文件存在，可读模式打开文件
            for line in f1:
                if "Atoms" in line:
                    frames += 1
                    timesteps.append(line)
            f1.close()
            return frames,timesteps
        else:
            raise IOError("这个路径下不存在输入的轨迹文件，好好检查下")

    # 提取轨迹帧数的方法
    def abstr_traj(self, frames):
        atomsum = 0
        timesteps = []
        f2 = open(self.trajfile,"r")
        atomsum = f2.readline()
        atomsum = int(atomsum)
        f2.seek(0)
        f3 = open("abstract_traj","a+")
        frames = [int(x) for x in frames]
        print(frames)
        f, timesteps = self.read_traj()

        for line in f2:
            for i in frames:
                timestep = timesteps[i-1]
                if timestep in line:
                    f3.write(str(atomsum) + "\n")
                    f3.write(timestep)
                    for i in range(atomsum):
                        line = f2.readline()
                        f3.write(line)

# 假如当前路径存在输出帧数同名称文件，删掉它！
if os.path.exists("abstract_traj"):
    os.remove("./abstract_traj")
trajfile = input("请输入要提取的轨迹文件名称：")
# 类的实例化
traj_inst = ReadTraj(trajfile)
frames, timesteps = traj_inst.read_traj()
frames = int(frames)
print("这个文件里一共有%s帧轨迹"%frames)

abstracted_frames = input("请输入您要提取的帧数，如1 2 3或者是一个范围如1-5：")
if "-" in abstracted_frames:
    list = abstracted_frames.split("-")
    new_list = np.arange(int(list[0]),int(list[1]) + 1, 1)
    new_list = new_list.tolist()
    traj_inst.abstr_traj(new_list)

else:
    new_list = abstracted_frames.split(" ")
    print(new_list)
    traj_inst.abstr_traj(new_list)


## 第二部分输出阴阳离子质心坐标

