from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, CallbackQuery , InlineKeyboardMarkup
from methods import *
from api import *





api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
bot_token =os.getenv('bot_token')


app = Client( 'bot' , api_id= api_id, api_hash=api_hash, bot_token= bot_token)

CurrentState = {
    'state':'',
    'Roundtrip': False
}


# welcome the user

@app.on_message(filters.regex('start') & filters.private)
def start(bot, message):
    bot.send_message(message.chat.id, f""" <b>Hi!  {message.from_user.mention},
                     
I am a flight search Bot 🌎
                     
You can search cheapest flight for your destination ✈️
                     
Let's start by typing   `menu`
                     </b>""", disable_web_page_preview = True )


# when user clicks on the book button

@app.on_message(filters.regex('menu'))
def book(app,message):
    button = [
        [InlineKeyboardButton('✈️ Book Cheapest Flight', callback_data="b_flight")],
        # [InlineKeyboardButton('🛠 Comming soon', callback_data="c_soon")]
    ]
    message.reply_text(
        text="**Please Choose a commad listed below**",
        reply_markup =InlineKeyboardMarkup(button)
    )


@app.on_message(filters.regex(r'^[A-Za-z]+$')) # this is big blunder because it get call when ever a string is input
def mssg(bot, message):
    try:
        # declaring global varible which need to be accessed in other functions
        global AirportList
        AirportList = () 
        print(CurrentState['state'])
        print('I m here')
        # if (len(i.Departure) == 0 ):  
        if (CurrentState['state'] == "GotDep"): 
            print("Hello")
            AirportList = getAirportList(message.text)
            print(AirportList)
            if (len(AirportList[0]) != 0):
                
                message.reply_text(
                text=f"""
    **Airports available in {message.text} city✈️
    **
    """
                )
                message.reply_text(
                text='\n'.join(f"**{i+1}. {name}**" for i, name in enumerate(AirportList[1]))
                )

                CurrentState['state'] = "nDep"
            # now I think I need to make a class and 

            elif(len(AirportList[0]) == 0):

                message.reply_text(
            text=f"**No Airpots Found. Enter a Valid City Name.**"
                )
        # elif(len(i.destination) == 0): 
        elif(CurrentState['state'] == "GotDes"):
            AirportList = getAirportList(message.text) 
            if (len(AirportList[0]) != 0):
                AirportList = getAirportList(message.text)
                message.reply_text(
                text=f"""
    **Airports available in {message.text} city✈️
    **
    """
                )
                message.reply_text(
                text='\n'.join(f"**{i+1}. {name}**" for i, name in enumerate(AirportList[1]))
                )

                CurrentState['state'] = "nDes" 

            elif(len(AirportList[0]) == 0):

                message.reply_text(
            text=f"**No Airpots Found. Enter a Valid City Name.**"
            ) 
        elif( CurrentState['state'] == 'VerfiedLocation' and (message.text).upper() == 'Y'):
            message.reply_text(
                text=f"""
    **Great! Now tell me how many seats you want to book? ✈️
     
Formart: `Adult,Children,infants`**
Example: `1,0,0`**  
    """#right now it only works for adults seating
                )
            CurrentState['state'] = 'GotSeats'
        elif( CurrentState['state'] == 'VerfiedLocation' and (message.text).upper() == 'N'):
            message.reply_text(
        text=f"**No problem, lets re-enter the Correct location.**")
            message.reply_text(text = """
**Booking Flight✈️

Please enter the Departure City

For example: `Cleveland`

**
""")
            CurrentState['state'] = "GotDep"
        elif(CurrentState['state'] == "GotFlighList"):
            message.reply_text(
                text=f"""
    **
To continue looking for new flight type `menu`
    **
    """)
      
        
    except:
        message.reply_text(
        text=f"**{message.from_user.mention} the message is not recognized at the moment.**"
    )

@app.on_message(filters.regex(r'^[0-9]+$'))
def pick_option(bot,message):
    
    try:
     
     if(len(message.text) == 1 or len(message.text) == 2):
        
    #         message.reply_text(
    #     text=f"**{message.from_user.mention} you picked an option {message.text}) {AirportList[1][int(message.text)-1]}**"
    # )
            if (CurrentState['state'] == "nDep"):
                i.setDeparture(AirportList[0][int(message.text)-1],AirportList[1][int(message.text)-1])
                message.reply_text(text = """
**Booking Flight✈️

Now Please enter the Destination City

For example: `Pittsburgh`

**
""")
                CurrentState['state'] = "GotDes" # departure location picked now next step
            # elif(len(i.destination) == 0):
            elif(CurrentState['state'] == "nDes"):
                i.setDestination(AirportList[0][int(message.text)-1],AirportList[1][int(message.text)-1])
                message.reply_text(
                text=f"""
    
    **{message.from_user.mention},

You have selected

Departure Location: `{i.Departure}`
Destination Location: `{i.destination}`

Is this correct (Y/N)?
    **
    """ 
                )
                CurrentState['state'] = "VerfiedLocation"
                
            elif(CurrentState['state'] == "GotFlighList"):
                message.reply_text(
                text=f"""
    **
To continue looking for new flight type `menu`
    **
    """)
     elif(CurrentState['state'] == "GotFlighList"):
                message.reply_text(
                text=f"""
    **
To continue looking for new flight type `menu`
    **
    """)
                
     else:
            message.reply_text(
        text=f"**{message.from_user.mention} the message is not recognized at the moment.**"
    )
            
    except:
        message.reply_text(
        text=f"**{message.from_user.mention} the message/digit is not recognized at the moment.**"
        
    )

@app.on_message(filters.regex(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"))
def getData(bot, message):
    date = message.text.split('/')
    
    gotdata = False
    if(CurrentState['state'] == "GotDate" and CurrentState['Roundtrip'] == False):
        i.setDepdate(date[2],date[0],date[1])
    elif(CurrentState['state'] == "GotDate" and CurrentState['Roundtrip'] == True):
        i.setDepdate(date[2],date[0],date[1])
        message.reply_text(
         text=f"""
    
    **{message.from_user.mention},

Now Tell me the Return date in correct format (month/day/year)

For example: `03/31/2025`

    **
    """ )
        CurrentState['state'] = "GotDepDate"
    elif (CurrentState['Roundtrip'] == True and CurrentState['state'] == "GotDepDate"):
        i.setRetdate(date[2],date[0],date[1])
    
    if(CurrentState['Roundtrip'] == False): 
        print("i m at oneway trip") 
        #get_price("CLE","PIT","2025-04-17","",1,0,0)
        data = get_price(i.DepCode,i.DesCode,i.Depdate,i.Retdate,i.adult,i.children,i.infants)
        gotdata = True
    elif(CurrentState['Roundtrip'] == True and CurrentState['state'] == "GotDepDate" and i.Retdate != ""):
        print(" I m at rounf trip")
        data = get_price(i.DepCode,i.DesCode,i.Depdate,i.Retdate,i.adult,i.children,i.infants)
        gotdata = True
    print(CurrentState['state'],gotdata)
    if gotdata:
        message.reply_text(
                    text=f"""
        **Lists of Cheapest Flighs ✈️

        **
        """
                    )
        flights = extract_flight_data(data)
        print(flights)
        message.reply_text(
                    text='\n'.join(f"**{BeauitfyData(name)} \n\n**" for i, name in enumerate(flights[:5])) # doesnt work if their is less then 5 flight that day or no fligths
                    )


        message.reply_text(
                    text=f"""
        **Above are the List of Cheapest flight for you Destiny✈️
At the moment this bot is not able to book flight directly
You can visit the airline website and book the flight at same price.

To continue looking for new flight type `menu`
        **
        """)

        CurrentState['state'] = "GotFlighList"
    # flights = extract_flight_data(data)
    # for flight in flights[:10]:
    #         print(flight)

 # get called when user enters the number of seats in format adult,children,infants
@app.on_message(filters.regex(r"\b\d{1,2},\d{1,2},\d{1,2}\b"))
def getSeats(bot, message):
    seat = message.text.split(',')
    i.setSeats(seat[0],seat[1],seat[2])   

    message.reply_text(
         text=f"""
**Booking Flight✈️

Please Choose an option from below:

** """ , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('One Way Trip', callback_data=f'o_trip')], [
                                              InlineKeyboardButton(' Round Trip ', callback_data=f'r_trip')]]))
    

@app.on_callback_query()
def callback_data(bot, x: CallbackQuery):
    # add option for user to check the iata code to the airpots name so they understand
    if 'b_flight' in x.data:
        # declaring global varible which need to be accessed in other functions
        global i
        text = """
**Booking Flight✈️

Please enter the Departure City

For example: `Cleveland`

**
"""
        CurrentState['state'] = "GotDep"
        bot.edit_message_text(
            chat_id=x.message.chat.id,
            text=text,
            message_id=x.message.id,
            
        )
        i = bookflight()

    # asking user for one way trip or round trip

    if 'o_trip' in x.data:
        
        text=f"""
    
    **{x.message.from_user.mention},

Now Tell me the Deparute date in correct format (month/day/year)

For example: `03/31/2025`

    **
    """ 
        bot.edit_message_text(
            chat_id=x.message.chat.id,
            text=text,
            message_id=x.message.id,
            
        )
    
        CurrentState['state'] = "GotDate"

    if 'r_trip' in x.data:
        CurrentState['Roundtrip'] = True
        text=f"""
    
    **{x.message.from_user.mention},

Now Tell me the Deparute date in correct format (month/day/year)

For example: `03/31/2025`

    **
    """ 
        bot.edit_message_text(
            chat_id=x.message.chat.id,
            text=text,
            message_id=x.message.id,
            
        )
        CurrentState['state'] = "GotDate"

    
# and Destination location

# For example: From California to Newyork


    
try:
    print("App initiated")
    
    app.run()
    
    
except Exception as e:
    print("Their was an error while initializing the app")

