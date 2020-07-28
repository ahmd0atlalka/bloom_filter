#אחמד טללקה-208900027  ו- ואסילה אלהואשלה -315589432
import string
import collections



def password_rules(password):
    print("the password is ",password)
    strengths = [['Length:', 'False',''],
                 ['Upper case letters','False',''],
                 ['Lower case letters', 'False',''],
                 ['Digits', 'False',''],
                 ['Symbols', 'False',''],
                 ['Digits & Symbols in the middle', 'False',''],
                 ['All letters', 'False',''],
                 ['All digits', 'False',''],
                 ['Repeated characters', 'False',''],
                 ['Consecutive uppercase letters', 'False',''],
                 ['Consecutive lowercase letters', 'False',''],
                 ['Consecutive digits', 'False',''],
                 ['Sequential letters', 'False',''],
                 ['Sequential digits', 'False','']]

    score = 0
    popup_msg="The password does not uphold to the standards due to:\n"




    if (len(password)>=8):
        score += (len(password)*4)
        strengths[0][1] = 'True [GOOD]'
        strengths[0][2]=str((len(password)*4))
    else:
        popup_msg+="Password is too short.\n"

    if any(x.isupper()for x in password):
        num_of_upper = [x for x in password if x.isupper()]
        score += (len(num_of_upper)*2)
        strengths[1][1] = 'True [GOOD]'
        strengths[1][2]=str(len(num_of_upper)*2)

    else:
        popup_msg+="Password contains no upper class letters.\n"

    if any(x.islower()for x in password):
        num_of_lower = [x for x in password if x.islower()]
        score += (len(num_of_lower)*2)
        strengths[2][1] = 'True [GOOD]'
        strengths[2][2] = str((len(num_of_lower)*2))
    else:
        popup_msg+="Password contains no lower class letters.\n"

    if any(x.isdigit()for x in password):
        num_of_digits = [x for x in password if x.isdigit()]
        score += (len(num_of_digits)*4)
        strengths[3][1] = 'True [GOOD]'
        strengths[3][2] = str((len(num_of_digits)*4))

    else:
        popup_msg+="Password contains no digits.\n"

###changed to check for special character
    if any(x in string.punctuation for x in password):
        num_of_signs = [x for x in password if x in string.punctuation]
        score += (len(num_of_signs)*6)
        strengths[4][1] = 'True [GOOD]'
        strengths[4][2] = str((len(num_of_signs)*6))
    else:
        popup_msg+="Password contains no special characters.\n"

    if len(password)>2:
        s = password[1:-1]
        if any(x.isalnum()for x in s) or any(x.isdigit()for x in s):
            num_of_signs = [x for x in password if x.isalnum()]
            num_of_signs += [x for x in password if x.isdigit()]
            score += (len(num_of_signs)*2)
            strengths[5][1] = 'True [GOOD]'
            strengths[5][2] = str((len(num_of_signs)*2))


## checking String
    if (password.isalpha()):
        score -= (len(password)/4)
        popup_msg+="Password is all letters.\n"
        strengths[6][1] = 'True [not GOOD]'
        strengths[6][2] = '-'+str((len(password)/4))

## checking string is all digits
    if(password.isdigit()):
        score -= (len(password)/4)
        popup_msg+="Password is all digits.\n"
        strengths[7][1] = 'True [not GOOD]'
        strengths[7][2] = '-'+str(((len(password) / 4)))

### checking for repeated characters
    results=0
    results = collections.Counter(password)
    for i in results:
        if results[i]>1:
            score -= results[i]*(results[i]-1)
            popup_msg+="Password has repeated characters.\n"
            strengths[8][1] = 'True [not GOOD]'
            strengths[8][2] = '-'+str((results[i]*(results[i]-1)))

### checking if there are consecutive uppercase characters
    countUpper=0
    l=len(password)
    for i in range(1,l-1):
        if (password[i] == password[i+1] and password[i].isupper()):
            countUpper += 1
        else:
            countUpper=1

        if countUpper>1:
            score -= countUpper*2
            popup_msg+="Password has consecutive uppercase letters.\n"
            strengths[9][1] = 'True [not GOOD]'
            strengths[9][2] = '-'-str((countUpper*2))

### checking if there are consecutive lowercase characters
    countLower=0
    for i in range(1,l-1):
        if(password[i] == password[i-1] and password[i].islower()):
            countLower += 1
        else:
            counterLower=1
        if countLower>1:
            score -= countLower*2
            popup_msg+="Password has consecutive lowercase letters.\n"
            strengths[10][1] = 'True [not GOOD]'
            strengths[10][2] = '-'+str((countLower*2))

##checking if there are sequential letters
    sequentialLettersCountUp=0
    sequentialLettersCountDown=0

    for letter in password:
        if ord(letter)<ord(letter)+1 and letter.isalpha():
            sequentialLettersCountUp+=1
        if ord(letter)>ord(letter)+1 and letter.isalpha():
            sequentialLettersCountDown+=1
    if sequentialLettersCountUp>=4 or sequentialLettersCountDown>=4:
        score -= (sequentialLettersCountUp+sequentialLettersCountDown)
        popup_msg+="Password has sequential letters.\n"
        strengths[11][1] = 'True [not GOOD]'
        strengths[11][2] = '-'+str(((sequentialLettersCountUp+sequentialLettersCountDown)))
        mandatory_violation=True

    sequentialDigitsCountUp=0
    sequentialDigitsCountDown=0

    for digit in password:
        if ord(digit)<ord(digit)+1 and digit.isdigit():
            sequentialDigitsCountUp+=1
        if ord(digit)>ord(digit)+1 and digit.isdigit():
            sequentialDigitsCountDown+=1
    if sequentialDigitsCountUp>=4 or sequentialDigitsCountDown>=4:
        score -= (sequentialDigitsCountUp+sequentialDigitsCountDown)
        strengths[12][1] = 'True [not GOOD]'
        strengths[12][2] = '-'+str(((sequentialDigitsCountUp+sequentialDigitsCountDown)))
        popup_msg+="Password has sequential digits.\n"
        mandatory_violation=True

    # set the score
    if score < 20:
        score_txt = 'Very Weak'
    elif score < 40:
        score_txt = 'Weak'
    elif score < 60:
        score_txt = 'Good'
    elif score < 80:
        score_txt = 'Strong'
    elif score >= 80:
        score_txt = 'Very Strong'

    return None, strengths, score_txt, popup_msg, mandatory_violation
