import string
def password_strength(password: str):
    score = 0
    variability = 0
    chars = list(password)

    not_long = True
    no_small = True
    no_big = True
    no_num = True
    no_spec = True


    if len(chars) >= 16:
        score += 5
        not_long = False
    elif len(chars) >= 12:
        score += 3
    elif len(chars) >= 8:
        score += 1

    if any(char.islower() for char in chars):
        variability += 1
        no_small = False    
    if any(char.isupper() for char in chars):
        variability += 1
        no_big = False
    if any(char.isdigit() for char in chars):
        variability += 1
        no_num = False
    if any(char in string.punctuation for char in chars):   
        variability += 1
        no_spec = False
  
    final_score = score * variability

    tips = []
    if not_long:
        tips.append("Make it longer (aim for 16 characters).")
    if no_small:
        tips.append("Add a lowercase letter.")
    if no_big:
        tips.append("Add an uppercase letter.")
    if no_num:
        tips.append("Add a number.")
    if no_spec:
        tips.append("Add a special character.")

    if final_score < 5:
        strength = "Weak"
    elif final_score < 10:
        strength = "Medium"
    elif final_score < 15:
        strength = "Strong"
    else:
        strength = "Very Strong"
        
    return strength, tips
