#!/usr/bin/env python

try:
    from hrpsys.hrpsys_config import *
    import OpenHRP
except:
    print "import without hrpsys"
    import rtm
    from rtm import *
    from OpenHRP import *
    import waitInput
    from waitInput import *
    import socket
    import time

import math

def init ():
    global hcf, initial_pose, hrpsys_version
    hcf = HrpsysConfigurator()
    hcf.getRTCList = hcf.getRTCListUnstable
    hcf.init ("Sample4LegRobot(Robot)0", "$(PROJECT_DIR)/../model/sample_4leg_robot.wrl")
    initial_pose = [0,  -0.378613,  0,  0.832038,  -0.452564,  0,
                    0,  -0.378613,  0,  0.832038,  -0.452564,  0,
                    0,  -0.378613,  0,  0.832038,  -0.452564,  0,
                    0,  -0.378613,  0,  0.832038,  -0.452564,  0,]
    hcf.seq_svc.setJointAngles(initial_pose, 2.0)
    hcf.waitInterpolation()
    # decrease zmp weight for arms
    abcp=hcf.abc_svc.getAutoBalancerParam()[1]
    abcp.leg_names = ['rleg', 'lleg', 'rarm', 'larm']
    hcf.abc_svc.setAutoBalancerParam(abcp)
    ggp = hcf.abc_svc.getGaitGeneratorParam()[1]
    ggp.zmp_weight_map = [1.0]*4
    ggp.default_step_height = 0.05
    hcf.abc_svc.setGaitGeneratorParam(ggp)
    hcf.startAutoBalancer()
    hrpsys_version = hcf.seq.ref.get_component_profile().version
    print("hrpsys_version = %s"%hrpsys_version)

def demoSetParameterAndStartST():
    print >> sys.stderr, "1. setParameter"
    stp_org = hcf.st_svc.getParameter()
    # for tpcc
    stp_org.k_tpcc_p=[0.2, 0.2]
    stp_org.k_tpcc_x=[4.0, 4.0]
    stp_org.k_brot_p=[0.0, 0.0]
    # for eefm
    stp_org.eefm_leg_inside_margin=71.12*1e-3
    stp_org.eefm_leg_outside_margin=71.12*1e-3
    stp_org.eefm_leg_front_margin=182.0*1e-3
    stp_org.eefm_leg_rear_margin=72.0*1e-3
    stp_org.eefm_k1=[-1.39899,-1.39899]
    stp_org.eefm_k2=[-0.386111,-0.386111]
    stp_org.eefm_k3=[-0.175068,-0.175068]
    stp_org.eefm_rot_damping_gain = [[20*1.6*1.5, 20*1.6*1.5, 1e5]]*4
    stp_org.eefm_pos_damping_gain = [[3500*50, 3500*50, 3500*1.0*1.5]]*4
    stp_org.is_ik_enable = [True]*4
    stp_org.is_feedback_control_enable = [True]*4
    stp_org.is_zmp_calc_enable = [True]*4
    stp_org.st_algorithm=OpenHRP.StabilizerService.EEFMQP
    hcf.st_svc.setParameter(stp_org)
    hcf.startStabilizer ()

def demo():
    init()

if __name__ == '__main__':
    demo()
