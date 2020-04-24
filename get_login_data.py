#!/home/navraj/anaconda3/bin/python
#SCRIPT TO EXTRACT THE LOGIN CREDETIALS FROM THE ROUTER SERVER LOG FILE

path_of_source = "ontlog.txt"
path_of_destination = "unprovision.txt"

index = {
    'month':0,
    'day':1,
    'time':2,
    'host': 3,
    'pon':10,
    'serial':12
}

def get_pon_port(pon):
    start1 = 'PON-'
    start2 = ''
    end = ':'
    pon = pon[pon.find(start1)+len(start1):pon.rfind(end)]
    pon = pon[pon.find(start2)+len(start2):pon.rfind(end)]
    pon = pon.replace("-","/")
    pon = pon+"/"
    return pon

def get_serial(serial):
    start = "="
    end = ","
    serial = serial[serial.find(start)+len(start):serial.rfind(end)]
    serial = f'{serial[:4]}:{serial[4:]}'
    return serial

def pre_processing():
    
    fread = open(path_of_source,"r")

    details = fread.readlines()

    list_data = []

    final_data = []

    for line in details:
        line = line.strip(" ").split(" ")
        line = [x for x in line if x and x!=',']
        list_data.append(line)

    for i in range(len(list_data)):
        time = list_data[i][index['month']]+" "+list_data[i][index['day']]+" "+list_data[i][index['time']]
        host = list_data[i][index['host']]+".subisu.net.np"
        pon = get_pon_port(list_data[i][index['pon']])
        serial = get_serial(list_data[i][index['serial']])
        final_data.append(f'{host},{pon},{serial},{time}')
    
    return final_data

def check_duplicates(final_data):
    unique_data = []
    host_dict={}
    host = []
    for i in range(len(final_data)):
        host = final_data[i].split(',')[0]
        host_dict.update({f'{host}':i})
    
    for key,value in host_dict.items():
        unique_data.append(final_data[value])
    return unique_data

def write_unprovision(unique_data):
    line = []
    fwrite = open(path_of_destination,"w")
    print("NEW DATA EXTRACTED FROM ONTLOG FILE :\n")
    for i in range(len(unique_data)):
        line = unique_data[i].split(",")
        line = f'{line[0]} {line[1]} {line[2]} {line[3]}'
        fwrite.write(line+'\n')
        print(line+'\n')

def main():
    print("Extracting data from ontlog file.......\n")
    final_data = pre_processing()
    print("Computing unique data in ontlog data.......\n")
    unique_data = check_duplicates(final_data)
    print("Writing new latest data in unprovison file\n")
    write_unprovision(unique_data)

main()
