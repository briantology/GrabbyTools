from imcsdk.imchandle import ImcHandle

# Create a connection handle
handle = ImcHandle("10.200.32.215", "admin", "C!sco123!")

# Login to the server
handle.login()

'''
Here IMC connects to and creates an object based on the class details of TopSystem, which is the
'chasis' and highest level of the Managed Objects Tree.  The next lower level of the heirarchy is
  the ComputeRackUnit which is basically the motherboard.  From there the daughter cards and a few other
  parts of UCS are represented and can be iterated over.

  Find more details on the Python library at https://ciscoucs.github.io/imcsdk_docs/imcsdk.html

  Find additional details on the CIMC API at the following links
  https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/c/sw/api/3_0/b_Cisco_IMC_api_301.html
  https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/c/sw/api/2-0/b_Cisco_IMC_api_2_0.html
  https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/c/sw/api/b_cimc_api_book.html

'''



CIMC_level_object = handle.query_classid(class_id='TopSystem')
motherboard_object = handle.query_classid(class_id='ComputeRackUnit')

# timezone = top_level_object.time_zone

for a in CIMC_level_object:
    timezone = a.time_zone
    server_time = a.current_time
    model_type = a.name
    assigned_IP = a.address
    server_mode = a.mode

    print(server_time)
    print(model_type)
    print(assigned_IP)
    print(server_mode)
    print(timezone)

for b in motherboard_object:
    available_memory = b.available_memory
    cimc_power_state = b.oper_power
    physical_cpu_count = b.num_of_cpus
    virtual_cpu_count = b.num_of_threads


# Logout from the server
handle.logout()






