lazy_recommended_movies=[2433, 515, 10, 2836, 922, 2205, 417, 929, 2724, 934, 936, 937, 682, 2865, 2227, 3123, 1591, 2487, 2233, 3004, 2877, 2367, 3008, 2240, 1858, 3137, 1860, 463, 719, 727, 988, 2140, 225, 2401, 3171, 999, 2663, 2281, 1898, 2156, 2670, 1267, 2420, 2166, 1274, 126, 2047]
movies_list=[]
with open("db/movies.dat", "r") as scan:
            for line in scan:
                iin=line.index(":")
                #print(iin)
                #break
                #print(line[0:(iin+1)])
                if(int(line[0:iin]) in lazy_recommended_movies):
                    lin=line.rindex("::")
                    movies_list.append(line[0:lin])
print(movies_list)
