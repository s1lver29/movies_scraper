import shutil

# Function to check free disk space
def check_disk_space(disk='/'):
    total, used, free = shutil.disk_usage(disk)
    free_gb = free // (2**30)  # Convert bytes to GB
    total_gb = total // (2**30)
    free_percentage = (free / total) * 100
    return free_gb, total_gb, free_percentage

# Main function that executes the disk space check
if __name__ == '__main__':
    free_gb, total_gb, free_percentage = check_disk_space()
    threshold = 10  # percentage threshold for low disk space
    if free_percentage < threshold:
        print(f'Внимание! Мало места на диске: {free_gb} ГБ свободно из {total_gb} ГБ')
    else:
        print(f'Места достаточно: {free_gb} ГБ свободно из {total_gb} ГБ')# Additional features can be added here: 
# - Adjust percentage threshold via command line arguments
# - Check multiple disks
# - Color-coded output