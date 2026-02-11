import psutil

print(psutil.cpu_percent(interval=1))        
print(psutil.cpu_percent(percpu=True))       
print(psutil.cpu_times())
