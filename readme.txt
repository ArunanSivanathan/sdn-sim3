main.cpp
----------------

28/06/2017: Command line option added. Now resolution time can be modified using command line.
current usage format is:
``usage: sdn_sim3 [options] <pcap_path> [<controller_id>] [-- <controller_options...>]
options:
 --verbose	verbose output
 --brief	brief output
 -r, --resolution=<T>	Logging resolution in Secs[default:60]''

 There are few things are noted in the todo list:
 1)allow to pass log directory as argument
 2)allow mac address file path to pass as an argument for Device classification app
 3)provide option to list the controllers and get help about each controllers: Currently, it has a static command line option.
 	When we are providing help for the controller, we may need to make the pcap as optional