import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os

# information on instance types to query
instance_library_types = ['c1.medium'  , 'c1.xlarge'  , \
                          'c3.large'   , 'c3.xlarge'  , 'c3.2xlarge' , 'c3.4xlarge', 'c3.8xlarge' , \
                          'cc2.8xlarge', 'cg1.4xlarge', 'cr1.8xlarge', 'g2.2xlarge', 'hi1.4xlarge', 'hs1.8xlarge', \
                          'i2.xlarge'  , 'i2.2xlarge' , 'i2.4xlarge' , 'i2.8xlarge', \
                          'm1.small'   , 'm1.medium'  , 'm1.large'   , 'm1.xlarge' , \
                          'm2.xlarge'  , 'm2.2xlarge' , 'm2.4xlarge' , \
                          'm3.medium'  , 'm3.large'   , 'm3.xlarge'  , 'm3.2xlarge', \
                          'r3.large', 'r3.xlarge', 'r3.2xlarge' , 'r3.4xlarge', 'r3.8xlarge', \
                          't1.micro'   , 't2.micro', 't2.small', 't2.medium', \
                          'c4.large'   , 'c4.xlarge', 'c4.2xlarge', 'c4.4xlarge', 'c4.8xlarge']

instance_library_vCPUs = [ 2,  8, \
                           2,  4,  8, 16, 32, \
                          32, 16, 32,  8, 16, 16, \
                           4,  8, 16, 32, \
                           1,  1,  2,  4, \
                           2,  4,  8, \
                           1,  2,  4,  8, \
                           2,  4,  8, 16, 32, \
                           1,  2,  1,  1, \
                           2,  4,  8, 16, 32]

instance_library_on_demand = [0.13, 0.52, \
                              0.105, 0.21, 0.42, 0.84, 1.68, \
                              2.00, 2.1, 3.5, 0.65, 3.1, 4.6, \
                              1.705, 3.410, 6.820, 0.853, \
                              0.044, 0.087, 0.175,  0.35, \
                              0.49, 0.98, 0.245, \
                              0.07, 0.14, 0.28, 0.56, \
                              0.175, 0.35, 0.7, 1.4, 2.8, \
                              0.02, 0.013, 0.026, 0.052, \
                              0.116, 0.232, 0.464, 0.928, 1.856] 

# list to save info on spot prices
instance_types = []
instance_vCPUs = []
current_prices = []
avg_prices = []
max_prices = []
current_prices_per_vCPU = []
avg_prices_per_vCPU = []
max_prices_per_vCPU = []
on_demand = []
on_demand_per_vCPU = []
current_pcts = []
avg_pcts = []

# counter for number instances that have spot pricing
num_instances = 0


# loop over instances and get spot prices
for i,instance in enumerate(instance_library_types):
    
    # ask starcluster to get the spot price info
    os.system('touch ' + instance + '.txt; touch ' + instance + '-error.txt')
    logfile = open(instance + '.txt', 'rw')
    errorfile = open(instance + '-error.txt', 'w')
    cmd_str = 'starcluster spothistory ' + instance + ' > spot-price-' + instance + '.txt'
    p1 = subprocess.Popen(cmd_str, stdout=logfile, stderr=errorfile, shell=True)
    p1.wait()
    
    # close and delete log and error files
    logfile.close()
    errorfile.close()
    os.system('rm ' + instance + '.txt')
    os.system('rm ' + instance + '-error.txt')

    # parse output and save spot price info to lists
    f = open('spot-price-' + instance + '.txt')
    data= f.readlines()
    if len(data) > 1:
        
        # print info on spot prices
        print instance + ' - On Demand Price: $' + str(instance_library_on_demand[i])
        print data[1].split()
        print data[2].split()
        print data[3].split()

        # save spot price info
        current_prices.append(float(data[1].split()[3][1:]))
        current_pcts.append(float(data[1].split()[3][1:]) / instance_library_on_demand[i] * 100.0)
        max_prices.append(float(data[2].split()[3][1:]))
        avg_prices.append(float(data[3].split()[3][1:]))
        avg_pcts.append(float(data[3].split()[3][1:]) / instance_library_on_demand[i] * 100.0)
        current_prices_per_vCPU.append(float(data[1].split()[3][1:]) / instance_library_vCPUs[i])
        max_prices_per_vCPU.append(float(data[2].split()[3][1:]) / instance_library_vCPUs[i])
        avg_prices_per_vCPU.append(float(data[3].split()[3][1:]) / instance_library_vCPUs[i])
        on_demand.append(instance_library_on_demand[i])
        on_demand_per_vCPU.append(instance_library_on_demand[i] / instance_library_vCPUs[i])
        instance_types.append(instance)

        # increment number of instances
        num_instances += 1

    # close and delete file
    f.close()
    os.system('rm spot-price-' + instance + '.txt')


# plot the current, max, and avg price per hour for each instance 
fig = plt.figure()
ax = plt.subplot(111)
w = 0.2
ax.bar(np.arange(num_instances), max_prices, width=w, color='r',align='center')
ax.bar(np.arange(num_instances)+w, avg_prices, width=w, color='b',align='center')
ax.bar(np.arange(num_instances)+2*w, current_prices, width=w, color='g',align='center')
ax.autoscale(tight=True)    
ax.set_xticks(np.arange(num_instances)+w/2.0)
ax.set_xticklabels(instance_types, rotation='vertical')
plt.ylim([0,1])
plt.ylabel('Price ($/hr)')
plt.tight_layout()
plt.savefig('instance-pricing.png')
#plt.show()


# plot the current, max, and avg price per hour per vCPU for each instance 
fig = plt.figure()
ax = plt.subplot(111)
w = 0.2
ax.bar(np.arange(num_instances), max_prices_per_vCPU, width=w, color='r',align='center')
ax.bar(np.arange(num_instances)+w, avg_prices_per_vCPU, width=w, color='b',align='center')
ax.bar(np.arange(num_instances)+2*w, current_prices_per_vCPU, width=w, color='g',align='center')
ax.autoscale(tight=True)    
ax.set_xticks(np.arange(num_instances)+w/2.0)
ax.set_xticklabels(instance_types, rotation='vertical')
plt.ylim([0,1])
plt.ylabel('Price ($/hr/vCPU)')
plt.tight_layout()
plt.savefig('instance-pricing-vCPU.png')
#plt.show()


# plot the current price per hour per vCPU and % on demand for each instance 
fig = plt.figure()
ax = plt.subplot(111)
w = 0.3
ax.bar(np.arange(num_instances), current_prices_per_vCPU, width=w, color='g',align='center')
ax.autoscale(tight=True)    
ax.set_xticks(np.arange(num_instances)+w/2.0)
ax.set_xticklabels(instance_types, rotation='vertical')
ax2 = ax.twinx()
ax2.bar(np.arange(num_instances)+w, current_pcts, width=w, color='b',align='center')
ax2.set_ylabel('% of on demand', color='b')
ax2.set_ylim([0,100])
ax.set_ylim([0,0.05])
ax.set_ylabel('Current Spot Price ($/hr/vCPU)', color='g')
plt.tight_layout()
plt.title('Current Spot Pricing per vCPU')
plt.savefig('current-spot-pricing-vCPU.png')
#plt.show()

# plot the current price per hour per vCPU and % on demand for each instance 
fig = plt.figure()
ax = plt.subplot(111)
w = 0.3
ax.bar(np.arange(num_instances), current_prices, width=w, color='g',align='center')
ax2 = ax.twinx()
ax2.bar(np.arange(num_instances)+w, current_pcts, width=w, color='b',align='center')
ax2.set_ylabel('% of on demand', color='b')
ax2.set_ylim([0,100])
ax.autoscale(tight=True)    
ax.set_xticks(np.arange(num_instances)+w/2.0)
ax.set_xticklabels(instance_types, rotation='vertical')
ax.set_ylim([0,0.5])
ax.set_ylabel('Current Spot Price ($/hr)', color='g')
plt.tight_layout()
plt.title('Current Spot Pricing')
plt.savefig('current-spot-pricing.png')
#plt.show()


# plot the on demand price per hour per vCPU for each instance 
fig = plt.figure()
ax = plt.subplot(111)
w = 0.5
ax.bar(np.arange(num_instances), on_demand_per_vCPU, width=w, color='g',align='center')
ax.autoscale(tight=True)    
ax.set_xticks(np.arange(num_instances)+w/2.0)
ax.set_xticklabels(instance_types, rotation='vertical')
#plt.ylim([0,0.03])
plt.ylabel('Price ($/hr/vCPU)')
plt.tight_layout()
plt.savefig('on-demand-pricing-vCPU.png')
#plt.show()

# plot the on demand price per hour per vCPU for each instance 
fig = plt.figure()
ax = plt.subplot(111)
w = 0.5
ax.bar(np.arange(num_instances), on_demand, width=w, color='g',align='center')
ax.autoscale(tight=True)    
ax.set_xticks(np.arange(num_instances)+w/2.0)
ax.set_xticklabels(instance_types, rotation='vertical')
#plt.ylim([0,0.25])
plt.ylabel('Price ($/hr)')
plt.tight_layout()
plt.savefig('on-demand-pricing.png')
#plt.show()

# plot the average price per hour per vCPU and % on demand for each instance 
fig = plt.figure()
ax = plt.subplot(111)
w = 0.3
ax.bar(np.arange(num_instances), avg_prices, width=w, color='g',align='center')
ax2 = ax.twinx()
ax2.bar(np.arange(num_instances)+w, avg_pcts, width=w, color='b',align='center')
ax2.set_ylabel('% of on demand', color='b')
ax2.set_ylim([0,100])
ax.autoscale(tight=True)    
ax.set_xticks(np.arange(num_instances)+w/2.0)
ax.set_xticklabels(instance_types, rotation='vertical')
ax.set_ylim([0,0.5])
ax.set_ylabel('Average Spot Price ($/hr)', color='g')
plt.tight_layout()
plt.title('Average Spot Pricing')
plt.savefig('average-spot-pricing.png')
#plt.show()

# plot the average price per hour per vCPU and % on demand for each instance 
fig = plt.figure()
ax = plt.subplot(111)
w = 0.3
ax.bar(np.arange(num_instances), avg_prices_per_vCPU, width=w, color='g',align='center')
ax.autoscale(tight=True)    
ax.set_xticks(np.arange(num_instances)+w/2.0)
ax.set_xticklabels(instance_types, rotation='vertical')
ax2 = ax.twinx()
ax2.bar(np.arange(num_instances)+w, avg_pcts, width=w, color='b',align='center')
ax2.set_ylabel('% of on demand', color='b')
ax2.set_ylim([0,100])
ax.set_ylim([0,0.05])
ax.set_ylabel('Average Spot Price ($/hr/vCPU)', color='g')
plt.tight_layout()
plt.title('Average Spot Pricing per vCPU')
plt.savefig('average-spot-pricing-vCPU.png')
#plt.show()
