pos = int(input('$'))
neg = int(input('$'))
neu = int(input('$'))

if pos > neg :
    overall = str('Positive : {} '.format(pos))
elif neu > neg:
    overall = str('Neutral : {} '.format(neu))
else:
    overall = str('Negative : {} '.format(neg))

print(overall)
