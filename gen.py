'''
This file contains the different lines used in the launch file.
'''

head_env = '<?xml version="1.0" encoding="UTF-8"?>\n<launch>\n	<arg name="environment" default="sauvc_pool"/>\n	<arg name="show_task4_balls" default="false" if="$(eval arg(\'environment\')==\'sauvc_pool\')"/>\n	<arg name="debug" default="false"/>\n	<arg name="gui" default="true"/>\n	<arg name="paused" default="true"/>\n	<arg name="use_sim_time" default="true"/>\n	<arg name="verbose" default="true"/>\n	<arg name="world_name" value="$(find uwv_env)/worlds/sauvc_pool.world" if="$(eval arg(\'environment\')==\'sauvc_pool\')"/>\n	<!-- Launching the world -->\n	<include file="$(find gazebo_ros)/launch/empty_world.launch">\n		<arg name="world_name" value="$(arg world_name)"/>\n		<arg name="debug" value="$(arg debug)"/>\n		<arg name="gui" value="$(arg gui)"/>\n		<arg name="paused" value="$(arg paused)"/>\n		<arg name="use_sim_time" value="$(arg use_sim_time)"/>\n		<arg name="verbose" value="$(arg verbose)"/>\n	</include>'
head1_env = '\t<group ns="/uwv/sauvc_pool" if="$(eval arg(\'environment\')==\'sauvc_pool\')">'
tail_env = '\t</group>\n</launch>'

head_control = '<?xml version="1.0" encoding="UTF-8"?>\n<launch>\n\t<arg name="vehicle" default="vec6"/>\n\t<arg name="round" default="2"/>\n\t<include file="$(find uwv_env)/launch/sauvc-pool-autogen.launch">\n\t\t<arg name="environment" value="sauvc_pool"/>\n\t\t<arg name="debug" value="false"/>\n\t\t<arg name="gui" value="true"/>\n\t\t<arg name="paused" value="true"/>\n\t\t<arg name="use_sim_time" value="true"/>\n\t\t<arg name="verbose" value="true"/>\n\t</include>\n\t<group ns="/vec6" if="$(eval arg(\'vehicle\')==\'vec6\')">\n\t\t<rosparam file="$(find uwv_control)/config/pid_gains.yaml"/>'
tail_control = '\t</group>\n</launch>'

def q_gate(pos):
	return f'\t\t<param name="q_gate_description" \n\t\t \tcommand="$(find xacro)/xacro $(find uwv_env)/urdf/sauvc_pool/q_gate.xacro" />\n\t\t<node name="$(anon spawn_q_gate)" \n\t\t\tpkg="gazebo_ros"\n\t\t\ttype="spawn_model" \n\t\t\trespawn="false"\n\t\t\toutput="screen"\n\t\t\targs="-urdf -model q_gate -param q_gate_description -x {pos[0]} -y {pos[1]} -Y {pos[2]}"/>'

def task1_gate(pos):
	return f'\t\t<param name="task1_gate_desc" \n\t\t\tcommand="$(find xacro)/xacro $(find uwv_env)/urdf/sauvc_pool/task1_gate.xacro" />\n\t\t<node name="$(anon spawn_task1_gate)" \n\t\t\tpkg="gazebo_ros"\n\t\t\ttype="spawn_model" \n\t\t\trespawn="false"\n\t\t\toutput="screen"\n\t\t\targs="-urdf -model task1_gate -param task1_gate_desc -x {pos[0]} -y {pos[1]} -z -0.5 -Y {pos[2]}"/>'

def task1_flare(pos):
	return f'\t\t<param name="task1_flare_desc" \n\t\t\tcommand="$(find xacro)/xacro $(find uwv_env)/urdf/sauvc_pool/task1_flare.xacro" />\n\t\t<node name="$(anon spawn_task1_flare)" \n\t\t\tpkg="gazebo_ros"\n\t\t\ttype="spawn_model" \n\t\t\trespawn="false"\n\t\t\toutput="screen"\n\t\t\targs="-urdf -model task1_flare -param task1_flare_desc -x {pos[0]} -y {pos[1]} -z -2 -Y {pos[2]}"/>'

def task2_mat(pos):
	return f'\t\t<param name="task2_mat_desc" \n\t\t\tcommand="$(find xacro)/xacro $(find uwv_env)/urdf/sauvc_pool/task2_mat.xacro" />\n\t\t<node name="$(anon spawn_task2_mat)" \n\t\t\tpkg="gazebo_ros"\n\t\t\ttype="spawn_model" \n\t\t\trespawn="false"\n\t\t\toutput="screen"\n\t\t\targs="-urdf -model task2_mat -param task2_mat_desc -x {-pos[0]} -y {-pos[1]} -z -2 -Y {pos[2]} -Y {pos[2]}"/>'

def task4_pinger(pos):
	return f'\t\t<param name="task4_pinger_desc" \n\t\t\tcommand="$(find xacro)/xacro $(find uwv_env)/urdf/sauvc_pool/task4_pinger.xacro" />\n\t\t<node name="$(anon spawn_task4_pinger)" \n\t\t\tpkg="gazebo_ros"\n\t\t\ttype="spawn_model" \n\t\t\trespawn="false"\n\t\t\toutput="screen"\n\t\t\targs="-urdf -model task4_pinger -param task4_pinger_desc -x {pos[0]} -y {pos[1]} -z -2 -Y {pos[2]}"/>'

def task4_no_pinger(pos):
	return f'\t\t<param name="task4_no_pinger_desc" \n\t\t\tcommand="$(find xacro)/xacro $(find uwv_env)/urdf/sauvc_pool/task4_no_pinger.xacro" />\n\t\t<node name="$(anon spawn_task4_no_pinger)" \n\t\t\tpkg="gazebo_ros"\n\t\t\ttype="spawn_model" \n\t\t\trespawn="false"\n\t\t\toutput="screen"\n\t\t\targs="-urdf -model task4_no_pinger -param task4_no_pinger_desc -x {pos[0]} -y {pos[1]} -z -2 -Y {pos[2]}"/>'

def start(pos):
	return f'<rosparam file="$(find uwv_control)/config/pid_gains.yaml"/>\n\t\n\t\t<param name="robot_description" \n\t\t\t   command="$(find xacro)/xacro $(find uwv_description)/urdf/vec6.xacro" />\n\t\t<node name="$(anon vec6_spawner)" \n\t\t\tpkg="gazebo_ros"\n\t\t\ttype="spawn_model" \n\t\t\trespawn="false"\n\t\t\toutput="screen"\n\t\t\targs="-urdf -model vec6 -param robot_description -x {pos[0]} -y {pos[1]} -Y {pos[2]}"/>'

if __name__ == "__main__":

	with open("/home/subzer0/uwv-ws/src/uwv-simulator/uwv_env/launch/launch-file.launch", "w") as f:
		print(head_env, end="\n\n", file=f)
		print(head1_env, end="\n\n", file=f)
		
		print(q_gate((0.1, 0, 0)), end="\n\n", file=f)
		print(task1_gate((0.2, 0, 0)), end="\n\n", file=f)
		print(task1_flare((0.3, 0, 0)), end="\n\n", file=f)
		# print(task2_mat((0, 0, 0)), end="\n\n", file=f)
		print(task4_pinger((0.4, 0, 0)), end="\n\n", file=f)
		print(task4_no_pinger((0.5, 0, 0)), end="\n\n", file=f)
		
		print(tail_env, end="\n\n", file=f)

