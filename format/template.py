data = [{'champion': 'lee-sin', 'kda': '3 / 4 / 4', 'status': 'Defeat', 'items': ['Goredrinker', 'Maw_of_Malmortius', "Mercury's_Treads"]}, 
        {'champion': 'yone', 'kda': '3 / 8 / 6', 'status': 'Defeat', 'items': ["Wit's_End", 'Infinity_Edge', 'Control_Ward', "Berserker's_Greaves", 'Immortal_Shieldbow']}, 
        {'champion': 'poppy', 'kda': '6 / 2 / 9', 'status': 'Victory', 'items': ['Turbo_Chemtank', 'Force_of_Nature', "Mercury's_Treads", 'Cloth_Armor', 'Kindlegem']}, 
        {'champion': 'azir', 'kda': '4 / 6 / 11', 'status': 'Victory', 'items': ['Shadowflame', "Luden's_Tempest", 'Needlessly_Large_Rod', 'Needlessly_Large_Rod', 'Tear_of_the_Goddess', "Sorcerer's_Shoes"]}, 
        {'champion': 'poppy', 'kda': '4 / 2 / 11', 'status': 'Defeat', 'items': ['Turbo_Chemtank', "Anathema's_Chains", 'Control_Ward', 'Ionian_Boots_of_Lucidity', 'Frozen_Heart']}, 
        {'champion': 'taliyah', 'kda': '2 / 7 / 10', 'status': 'Defeat', 'items': ['Corrupting_Potion', "Luden's_Tempest", 'Void_Staff', "Sorcerer's_Shoes", "Seraph's_Embrace"]}, 
        {'champion': 'taliyah', 'kda': '6 / 2 / 15', 'status': 'Victory', 'items': ['Corrupting_Potion', "Seraph's_Embrace", 'Needlessly_Large_Rod', "Luden's_Tempest", 'Void_Staff', "Sorcerer's_Shoes"]}, 
        {'champion': 'taliyah', 'kda': '6 / 6 / 5', 'status': 'Defeat', 'items': ['Crown_of_the_Shattered_Queen', "Doran's_Ring", "Zhonya's_Hourglass", "Seraph's_Embrace", 'Ionian_Boots_of_Lucidity', 'Dark_Seal']}, 
        {'champion': 'fiora', 'kda': '4 / 2 / 3', 'status': 'Defeat', 'items': ['Ionian_Boots_of_Lucidity', 'Divine_Sunderer', 'Ravenous_Hydra', "Doran's_Blade", "Caulfield's_Warhammer", 'Cull']}, 
        {'champion': 'taliyah', 'kda': '8 / 9 / 5', 'status': 'Defeat', 'items': ['Corrupting_Potion', "Luden's_Tempest", "Seraph's_Embrace", 'Void_Staff', "Sorcerer's_Shoes", "Mejai's_Soulstealer"]}, 
        {'champion': 'akali', 'kda': '12 / 3 / 11', 'status': 'Victory', 'items': ['Hextech_Rocketbelt', 'Void_Staff', "Zhonya's_Hourglass", 'Amplifying_Tome', "Sorcerer's_Shoes", "Doran's_Ring"]}, 
        {'champion': 'ryze', 'kda': '2 / 0 / 3', 'status': 'Victory', 'items': ['Corrupting_Potion', 'Perfectly_Timed_Stopwatch', 'Crown_of_the_Shattered_Queen', 'Tear_of_the_Goddess', 'Ionian_Boots_of_Lucidity']}, 
        {'champion': 'yone', 'kda': '9 / 3 / 4', 'status': 'Victory', 'items': ['Immortal_Shieldbow', 'Guardian_Angel', "Berserker's_Greaves", 'Infinity_Edge', "Wit's_End"]}]


def getHTMLfile(data):
        def decryptChampName(name):
                if "-" in name:
                        names = name.split("-")
                        nams = []
                        for nam in names:
                                nam = nam.capitalize()
                                nams.append(nam)
                        champ = ' '.join(nams)
                        return champ
                else:
                        return name.capitalize()
        name = decryptChampName(data['champion'])
        items = []
        for item in data['items']:
                item_html = f'<img src="../items/{item}.png" alt="" class="item"/>'
                items.append(item_html)
        items_html = ''.join(items)
        style = '''<style>
        @font-face {
            font-family: font;
            src: url(font.otf);
          }
        * {
            box-sizing: border-box;
            padding: 0;
            margin: 0;
            font-family: font;
        }
        .imageContainer {
            width: 100vw;
            height: 100vh;
        }
        .imageContainer > img {
            position: relative;
            width: 100%;
            height: 100%;
        }
        .textContainer {
            position: absolute;
            width: 35%;
            height: 90%;
            background: linear-gradient(to right bottom, rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.3));
            backdrop-filter: blur(0,2rem);
            left: 100px;
            bottom: 50px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            flex-direction: column;
            justify-content: flex-start;
            padding-top: 50px;
        }
        .items {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            width: 70%;
            margin-top: 50px;
        }
        .item {
            width: 100px;
            height: 100px;
            border-radius: 16px;
        }
        .status {
            font-size: 5rem;
        }
        .Defeat {
            color: #e74c3c;
        }
        .Victory {
            color: #27ae60;
        }
        .kda {
            font-size: 4rem;
            color: #f1c40f;
        }
        .champ {
            font-size: 4rem;
            color: #9b59b6;
        }
    </style>'''
        html = f'''
             <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cac</title>
    {style}
</head>
<body>
    <div class="imageContainer">
        <img src="../images/{data["champion"]}.png" alt=""/>
        <div class="textContainer">
            <div class="status {data["status"]}">{data["status"]}</div>
            <div class="champ">{name}</div>
            <div class="kda">{data["kda"]}</div>
            <div class="items">
                {items_html}
            </div>
        </div>
    </div>
    
</body>
</html>   
        '''
        return html

