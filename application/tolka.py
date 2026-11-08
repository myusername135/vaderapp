def tolka(indata):
    dag = []
    datum = indata["daily"]["time"]
    hogsta_temp = indata["daily"]["temperature_2m_max"]
    lagsta_temp = indata["daily"]["temperature_2m_min"]
    nederbord = indata["daily"]["precipitation_sum"]
    for x in range(len(datum)):
        dag.append({"datum": datum[x], "max": hogsta_temp[x], "min": lagsta_temp[x], "nederbord": nederbord[x]})
    return dag
