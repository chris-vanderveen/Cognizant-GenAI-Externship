def main():
    pwd = input("Please input a password: ")
    min_length = 8
    has_upper = False
    has_lower = False
    has_special = False
    has_digit = False
    is_long_enough = len(pwd) >= min_length

    for char in pwd:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        # Check if it's not alphanumeric and not whitespace
        # This way, only symbols/punctuation count as special
        elif not char.isalnum() and not char.isspace():
            has_special = True

    # Check if all conditions are met
    is_strong = all([has_upper, has_lower, has_digit, has_special, is_long_enough])

    if is_strong:
        print("Your password is strong! 💪")
    else:
        # Find out what's missing and assemble a message
        missing_requirements = []

        # Check each requirement and add to the list if missing
        if not is_long_enough:
            missing_requirements.append(f"to be at least {min_length} characters long")
        if not has_upper:
            missing_requirements.append("at least one uppercase letter")
        if not has_lower:
            missing_requirements.append("at least one lowercase letter")
        if not has_digit:
            missing_requirements.append("at least one number")
        if not has_special:
            missing_requirements.append("at least one special character (e.g., !@#$%)")

        # Construct the message based on the number of missing items
        message_start = "Your password needs "
        
        if len(missing_requirements) == 0:
             print("Password validation error.") 
        elif len(missing_requirements) == 1:
            # Only one requirement missing
            message = message_start + missing_requirements[0] + "."
        elif len(missing_requirements) == 2:
            # Two requirements missing - join with "and"
            message = message_start + missing_requirements[0] + " and " + missing_requirements[1] + "."
        else:
            # Join all but the last item with ", "
            most_requirements = ", ".join(missing_requirements[:-1])
            # Add the last item with ", and "
            message = message_start + most_requirements + ", and " + missing_requirements[-1] + "."

        print(message)

if __name__ == "__main__":
    main()
