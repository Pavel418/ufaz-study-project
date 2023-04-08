subways = (["28 / Jafar Jabbarli", 40.38278310227317, 49.84679519744824], ["Sahil", 40.371974998746005, 49.84405620938562], ["Icherisheher", 40.366106296864864, 49.83165260854011],
            ["Nizami", 40.37966172913042, 49.83028696791216], ["Elmler", 40.37519653577367, 49.8144159839544], 
            ["Inshaatcilar", 40.390286712687086, 49.80266890649604], ["Khatai", 40.38367997016057, 49.87198948221093],
            ["Ganjlik", 40.400695138059746, 49.85158561279074], ["Nariman Narimanov", 40.40564344658408, 49.87084158387418,],
            ["Ulduz", 40.40564344658408, 49.87084158387418], ["Gara Garayev", 40.42279507348184, 49.93486614333679],
            ["Neftchiler", 40.41035399448429, 49.943230123780445], ["Khalglar Dostlughu", 40.39809074592212, 49.95193378892042],
            ["Ahmadli", 40.38683318229922, 49.952825746241025], ["Hazi Aslanov", 40.374117636572144, 49.95359028108725], 
            ["Memar Ajami", 40.41279738674918, 49.81461894228935], ["Avtovagzal", 40.42419787524228, 49.79508704280422], 
            ["Nasimi", 40.42419787524228, 49.79508704280422], ["8 noyabr", 40.40357644851948, 49.82034830011121], 
            ["Azadlig", 40.42707247607273, 49.84235424019779], ["Darnaghul", 40.42647774116251, 49.86136528902999],
            ["Khojasan", 40.42191793220399, 49.778680247211376], ["Koroghlu", 40.42063419443794, 49.91767945403461],
            ["Bakmil", 40.41511995175986, 49.878749137199726], ["20 yanvar", 40.40437043171568, 49.808554290309566])


distances = []
for i in range(len(houses)):
    distances.append([])
    for j in range(len(subways)):
        
        delta_x = houses[i][0]-subways[j][1]
        delta_y = houses[i][1]-subways[j][2]
        distance = (delta_x**2 + delta_y**2)**(0.5)
        distances[i].append(distance)
    min_idx = distances[i].index(min(distances[i]))
    print('closest subway to house number', i, ' at ', houses[i], 'is subway ', subways[min_idx], ' number ', min_idx, ' at ',  min(distances[i])
