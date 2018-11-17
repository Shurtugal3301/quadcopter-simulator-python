# Examples Go-to-Point File
# Christopher Banks
# 10/14/18
# This file provides an example of how to send commands to the Robotarium for moving a number of quadcopters from one pose
# to another.
from utilities.robotarium_simulation_builder import RobotariumEnvironment
from utilities.interpolation import spline_interpolation, extract_points
import numpy as np

TIMEOUT = False

if __name__ == "__main__":
    # creates robotarium object, indictate if user would like to save data
    robotarium = RobotariumEnvironment(save_data=True)

    # robotarium object sets a random number of agents to be created

    # sets the number of agents
    robotarium.number_of_agents = 3

    # iterate until time limit is reached, the max time our quadcopters can run is 5 minutes so experiments will be
    # limited to that time

    # Iteration method is arbitrary, we will provide a function to check if experiment will timeout however

    # if specific initial poses are desired, set robotarium.initial_poses
    #robotarium.initial_poses = np.array([[0.1, 0.1, -0.5], [1, 0.3, -1.3], [1, 1, -1.2]])

    # instantiates Robotarium and initializes quadcopters at random poses if initial_poses is not set


    x_desired = np.array([[[0.2, 0.2, -0.5], [0.5, -0.5, -0.8], [0.2, 0.2, -0.9], [1, 0.4, -1.3]],
                         [[0.4, 0.4, -0.7], [0.1, 0.1, -0.4], [-1.1, 0.2, -.3], [-0.1, -0.3, -0.6]],
                         [[1.1, 1.2, -1.2], [0.2, 0.5, -0.8], [-0.1, -0.3, -0.6],[-0.7, 0.3, -0.7]]])

    i = 0
    time_lim = 500

    point_spline_for_quads = dict()
    index_update = dict()
    init_pose = np.zeros((robotarium.number_of_agents, 3))
    for i in range(robotarium.number_of_agents):
       points = np.stack((x_desired[i]))
       spline_coeffs_for_quad = spline_interpolation(points)
       spline_for_quads = extract_points(spline_coeffs_for_quad)
       point_spline_for_quads[i] = spline_for_quads
       print("spline: ", spline_for_quads)
       init_pose[i] = point_spline_for_quads[i][0][0, :]
       index_update[i] = 0
    #robotarium.initial_poses = np.array([[-1.0, 1.0, -0.8],
    #                                     [-1.0, -0.3, -0.5]])

    robotarium.initial_poses = init_pose

    robotarium.build()

    point_update  = np.zeros((robotarium.number_of_agents, 3))
    while i < time_lim:
        # retrieve quadcopter poses (numpy array, n x m x 3) where n is the quadcopter index
        #x = robotarium.get_quadcopter_poses()

        # Insert your code here!!
        for j in range(robotarium.number_of_agents):
            #print("agent: ", j)
            #print("desired:", x_desired[j])
            desired_point = point_spline_for_quads[j][index_update[j]]
            if index_update[j] < point_spline_for_quads[j].shape[0] - 1:
                index_update[j] += 1
            else:
                index_update[j] = point_spline_for_quads[j].shape[0] - 1
            point_update[j] = desired_point[0, :]


        # Set desired pose
        robotarium.set_desired_poses(point_update)

        # send pose commands to robotarium
        robotarium.update_poses()
        print("poses: ", robotarium.poses)

        i += 1
        # also users can self limit runtime of program
        if robotarium.run_time() > 60:
            TIMEOUT = True





