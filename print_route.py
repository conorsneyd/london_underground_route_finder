def print_route(route): 
    #convert route into user-friendly text
    changes = []
    for i in range(len(route[-1])-1):
        #iterate through list of stations and create list of line changes (including checking for edge cases which create false changes or require additional changes)
        current_line = route[-1][i][1]
        next_line = route[-1][i + 1][1]
        current_direction = route[-1][i][2]
        next_direction = route[-1][i + 1][2]
        current_station = route[-1][i][0]
        next_station = None
        previous_station = None
        previous_previous_station = None
        if i < len(route[-1]) - 1:
            next_station = route[-1][i + 1][0]
        if i > 0:
            previous_station = route[-1][i - 1][0]
        if i > 1:
            previous_previous_station = route[-1][i - 2][0]
        false_change = check_for_false_changes(current_station, next_station, previous_station, current_line)
        additional_change = check_for_additional_changes(current_station, next_station, previous_station, previous_previous_station, current_line)
        if (current_line != next_line or current_direction != next_direction or additional_change == True) and (false_change == False):
            changes.append((current_station, next_line, next_direction))
    starting_line = route[-1][0][1]
    starting_station = route[-1][0][0]
    starting_direction = route[-1][0][2]
    final_station = route[-1][-1][0]
    final_direction = route[-1][-1][2]
    directions = ""

    if changes:
        #iterate through list of changes to construct user-friendly directions
        first_change_station = changes[0][0]
        starting_line_towards_station = format_line(starting_line, starting_direction, starting_station, first_change_station)
        directions += f"<ul><li>Take the {starting_line_towards_station} from {starting_station} to {first_change_station}.</li><br>"
        for i in range(len(changes)-1):
            change_station = changes[i][0]
            change_line = changes[i][1]
            change_direction = changes[i][2]
            next_change_station = changes[i+1][0]
            change_line_towards_station = format_line(change_line, change_direction, change_station, next_change_station)
            directions += f"<li>At {change_station}, change to the {change_line_towards_station}.</li><br>"
            directions += f"<li>Take the {change_line} line to {next_change_station}.</li><br>"
        final_change_station = changes[-1][0]
        final_change_line = changes[-1][1]
        final_change_direction = changes[-1][2]
        final_change_line_towards_station = format_line(final_change_line, final_change_direction, final_change_station, final_station)
        directions += f"<li>At {final_change_station}, change to the {final_change_line_towards_station}.</li><br>"
        directions += f"<li>Take the {final_change_line} line to {final_station}.</li></ul>"
    else:
        #if no changes, return single line of directions
        starting_line_towards_station = format_line(starting_line, final_direction, starting_station, final_station)
        directions += f"<ul><li>Take the {starting_line_towards_station} from {starting_station} to {final_station}.</li></ul>"
    return directions, starting_station, final_station

def format_line(line, direction, current_station, change_station):
    #add '(towards X)' to line name by checking direction of travel (accounting for edge cases)
    if line == "Bakerloo":
        if direction == 1:
            return("Bakerloo line (towards Elephant and Castle)")
        elif direction == 2:
            return("Bakerloo line (towards Harrow and Wealdstone)")
    elif line == "Central":
        if direction == 1:
            if change_station in ["Wanstead", "Redbridge", "Gants Hill", "Newbury Park", "Barkingside", "Fairlop", "Hainault", "Grange Hill", "Chigwell", "Roding Valley"]:
                return("Central line (towards Roding Valley)")
            elif change_station in ["Snaresbrook", "South Woodford", "Woodford", "Buckhurst Hill", "Loughton", "Debden", "Theydon Bois", "Epping"]:
                return("Central line (towards Epping)")
            else:
                return("Central line (towards Epping or Roding Valley)")
        elif direction == 2:
            if change_station in ["West Acton", "Ealing Broadway"]:
                return("Central line (towards Ealing Broadway)")
            elif change_station in ["Park Royal", "Hanger Lane", "Perivale", "Greenford", "Northolt", "South Ruislip", "Ruislip Gardens", "West Ruislip"]:
                return("Central line (towards West Ruislip)")
            else:
                return("Central line (towards Ealing Broadway or West Ruislip)")  
    elif line == "Circle":
        if direction == 1:
            return("Circle line (clockwise towards Edgware Road)")
        elif direction == 2:
            return("Circle line (anticlockwise towards Hammersmith)")
    elif line == "Jubilee":
        if direction == 1:
            return("Jubilee line (towards Stratford)")
        elif direction == 2:
            return("Jubilee line (towards Stanmore)")
    elif line == "District":
        if direction == 1:
            if change_station in ["Chiswick Park", "Acton Town", "Ealing Common", "Ealing Broadway"]:
                return("District line (towards Ealing Broadway)")
            elif change_station in ["Gunnersby", "Kew Gardens", "Richmond"]:
                return("District line (towards Richmond)")
            elif change_station in ["Turnham Green", "Stamford Brook", "Ravenscourt Park", "Hammersmith", "Barons Court", "West Kensington"]:
                return("District line (towards Ealing Broadway or Richmond)")
            elif change_station in ["High Street Kensington", "Notting Hill Gate", "Bayswater", "Paddington", "Edgware Road"]:
                return("District line (towards Edgware Road)")
            elif change_station == "Kensington Olympia":
                return ("District line (towards Kensington Olympia)")
            elif change_station == "Earl's Court":
                if current_station in ["West Brompton", "Fulham Broadway", "Parsons Green", "Putney Bridge", "East Putney", "Southfields", "Wimbeldon Park", "Wimbeldon"]:
                    return("District line (towards Edgware Road or Upminster)")
                else:
                    return("District line (towards Ealing Broadway, Richmond or Wimbeldon)")
            else:
                    return("District line (towards Ealing Broadway, Richmond or Wimbeldon)")  
        elif direction == 2:
            if change_station in ["West Brompton", "Fulham Broadway", "Parsons Green", "Putney Bridge", "East Putney", "Southfields", "Wimbeldon Park", "Wimbeldon"]:
                return ("District line (towards Wimbeldon)")
            elif change_station in ["Edgware Road", "Paddington", "Bayswater", "Notting Hill Gate", "High Street Kensington"]:
                return ("District line (towards Upminster or Wimbeldon)")            
            elif change_station == "Earl's Court":
                if current_station in ["Edgware Road", "Paddington", "Bayswater", "Notting Hill Gate", "High Street Kensington"]:
                    return ("District line (towards Upminster or Wimbeldon)")
                else:
                    return("District line (towards Upminster)")
            else:
                return ("District line (towards Upminster)")
        else:
            return("District line")
    elif line == "Hammersmith and City":
        if direction == 1:
            if change_station in ["Aldgate East", "Whitechapel", "Stepney Green", "Mile End", "Bow Road", "Bromley-by-Bow", "West Ham", "Plaistow", "Upton Park", "East Ham", "Barking"]:
                return("Hammersmith and City line (towards Hammersmith)")
            else:
                return("Hammersmith and City line (towards Barking)")
        elif direction == 2:
            if change_station in ["Aldgate East", "Whitechapel", "Stepney Green", "Mile End", "Bow Road", "Bromley-by-Bow", "West Ham", "Plaistow", "Upton Park", "East Ham", "Barking"]:
                return("Hammersmith and City line (towards Barking)")
            else:
                return("Hammersmith and City line (towards Hammersmith)")
    elif line == "Metropolitan":
        if direction == 1:
            return("Metropolitan line (towards Aldgate)")
        elif direction == 2:
            if change_station == "Chesham":
                return("Metropolitan line (towards Chesham)")
            elif change_station == "Amersham":
                return("Metropolitan line (towards Amersham)")
            elif change_station in ["Rickmansworth", "Chorleywood", "Chalfont and Latimer"]:
                return("Metropolitan line (towards Amersham or Chesham)")
            elif change_station in ["Croxley", "Watford"]:
                return("Metropolitan line (towards Watford)")
            elif change_station in ["North Harrow", "Pinner", "Northwood Hills", "Northwood", "Moor Park"]:
                return ("Metropolitan line (towards Amersham, Chesham or Watford)")
            elif change_station in ["West Harrow", "Rayners Lane", "Eastcoate", "Ruislip Manor", "Ruislip", "Ickenham", "Hillingdon", "Uxbridge"]:
                return ("Metropolitan line (towards Uxbridge)")
            else:
                return ("Metropolitan line (towards Amersham, Chesham, Watford or Uxbridge)")
    elif line == "Northern":
        line_and_direction = ""
        branch = ")"
        if change_station in ["Mornington Crescent", "Warren Street", "Goodge Street", "Tottenham Court Road", "Leicester Square", "Charing Cross", "Embankment", "Waterloo"]:
            branch = " via Charing Cross)"
        elif change_station in ["King's Cross St Pancras", "Angel", "Old Street", "Moorgate", "Bank", "London Bridge", "Borough", "Elephant and Castle"]:
            branch = " via Bank)"
        if direction == 1:
            if change_station in ["Nine Elms", "Battersea Power Station"]:
                line_and_direction = "Northern line (towards Battersea Power Station"
            elif change_station in ["King's Cross St Pancras", "Angel", "Old Street", "Moorgate", "Bank", "London Bridge", "Borough", "Elephant and Castle", "Oval", "Stockwell", "Clapham North", "Clapham Common", "Clapham South", "Balham", "Tooting Bec", "Tooting Broadway", "Colliers Wood", "South Wimbeldon", "Morden"]:
                line_and_direction = "Northern line (towards Morden"
            elif current_station in ["King's Cross St Pancras", "Angel", "Old Street", "Moorgate", "Bank", "London Bridge", "Borough", "Elephant and Castle"] and change_station == "Kennington":
                line_and_direction = "Northern line (towards Morden"
            else:
                line_and_direction = "Northern line (towards Battersea Power Station or Morden"
        elif direction == 2:
            if change_station in ["Chalk Farm", "Belsize Park", "Hampstead", "Golders Green", "Brent Cross", "Hendon Central", "Colindale", "Burnt Oak", "Edgware"]:
                line_and_direction = "Northern line (towards Edgware"
            elif change_station in ["Kentish Town", "Tufnell Park", "Archway", "Highgate", "East Finchley", "Finchley Central"]:
                line_and_direction = "Northern line (towards High Barnet or Mill Hill East"
            elif change_station in ["West Finchley", "Woodside Park", "Totteridge and Whetstone", "High Barnet"]:
                    line_and_direction = "Northern line (towards High Barnet"
            elif change_station == "Mill Hill East":
                    line_and_direction = "Northern line (towards Mill Hill East"
            else:
                line_and_direction = "Northern line (towards Edgware, High Barnet or Mill Hill East"
        return line_and_direction + branch
    elif line == "Piccadilly":
        if direction == 1:
            if current_station in ["Rayners Lane", "Eastcoate", "Ruislip Manor", "Ruislip", "Ickenham", "Hillingdon", "Uxbridge"]:
                return("Piccadilly line (towards Cockfosters)")
            else:
                if change_station in ["South Ealing", "Northfields", "Boston Manor", "Osterley", "Hounslow East", "Hounslow Central", "Hounslow West", "Hatton Cross", "Heathrow Terminals 2 and 3"]:
                    if current_station == "Heathrow Terminal 4":
                        return("Piccadilly line (towards Heathrow Terminals 2 and 3)")
                    return("Piccadilly line (towards Heathrow Terminals 2, 3, 4 or 5)")
                elif change_station == "Heathrow Terminal 4":
                    return("Piccadilly line (towards Heathrow Terminal 4)")
                elif change_station == "Heathrow Terminal 5":
                    return("Piccadilly line (towards Heathrow Terminal 5)")
                elif change_station in ["Ealing Common", "North Ealing", "Park Royal", "Alperton", "Sudbury Town", "Sudbury Hill", "South Harrow", "Rayners Lane", "Eastcoate", "Ruislip Manor", "Ruislip", "Ickenham", "Hillingdon", "Uxbridge"]:
                    return("Piccadilly line (towards Uxbridge)")
                else:
                    return("Piccadilly line (towards Uxbridge or Heathrow Terminals)")
        if direction == 2:
            if change_station in ["Rayners Lane", "Eastcoate", "Ruislip Manor", "Ruislip", "Ickenham", "Hillingdon", "Uxbridge"]:
                return("Piccadilly line (towards Uxbridge)")
            else:
                return("Piccadilly line (towards Cockfosters)")
    elif line == "Victoria":
        if direction == 1:
            return("Victoria line (towards Brixton)")
        elif direction == 2:
            return("Victoria line (towards Walthamstow Central)")
    return (line + " line")
    
def check_for_additional_changes(current_station, next_station, previous_station, previous_previous_station, current_line):
    #check for edge cases requiring an additional change to be added
    if current_line == "Central":
        if previous_station == "Roding Valley" and next_station == "Buckhurst Hill":
            return True 
    elif current_line == "Circle":
        if current_station == "Paddington" and previous_station == "Bayswater" and next_station != "Edgware Road":
            return True
        elif current_station == "Edgware Road" and previous_previous_station == "Bayswater":
            return True
        elif current_station == "Paddington" and previous_previous_station == "Baker Street" and next_station == "Bayswater":
            return True
    elif current_line == "District":
        if previous_station == "High Street Kensington" and next_station == "Gloucester Road":
            return True
        elif previous_station == "Gloucester Road" and next_station == "High Street Kensington":
            return True
        elif previous_station == "West Kensington" and next_station == "West Brompton":
            return True
        elif previous_station == "West Brompton" and next_station == "Kensington Olympia":
            return True
        elif previous_station == "Kensington Olympia" and next_station == "West Brompton":
            return True
        elif previous_station == "West Brompton" and next_station == "West Kensington":
            return True
        elif previous_station == "West Kensington" and next_station == "West Brompton":
            return True
    elif current_line == "Northern":
        if previous_station == "Elephant and Castle" and next_station == "Nine Elms":
            return True
        elif previous_station == "Nine Elms" and next_station == "Elephant and Castle":
            return True
    elif current_line == "Piccadilly":
        if next_station == "Heathrow Terminal 5" and previous_station == "Heathrow Terminal 4":
            return True
        elif next_station == "Heathrow Terminal 4" and previous_station == "Heathrow Terminal 5":
            return True
    else:
        return False
    
def check_for_false_changes(current_station, next_station, previous_station, current_line):
    #check for edge cases causing a false change
    if current_line == "District":
        if previous_station == "High Street Kensington" and next_station == "West Kensington":
            return True
        elif previous_station == "High Street Kensington" and next_station == "Kensington Olympia":
            return True
        elif previous_station == "Kensington Olympia" and next_station == "High Street Kensington":
            return True 
        elif previous_station == "West Brompton" and next_station == "Gloucester Road":
            return True
        elif previous_station == "Gloucester Road" and next_station == "West Brompton":
            return True 
    elif current_line == "Hammersmith and City":
        if current_station == "Aldgate East":
            return True
    elif current_line == "Piccadilly":
        if current_station == "Rayners Lane" and (next_station == "Eastcoate" or next_station == "South Harrow"):
            return True
    elif current_line == "Victoria":
        if current_station == "Euston"  or current_station == "Warren Street":
            return True
        
    return False