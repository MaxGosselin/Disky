import disky

print 'Welcome to disky!'
print 'Would you like to run Disky in fullscreen (recommended)? (Yes/No)'
answer = raw_input()
if isinstance(answer, str):
    if (answer) in ['Yes', 'yes', 'Y', 'y', 'yse']:
        A2 = disky.Disky(None)
    else:
        print 'Enter the desired resolution, in the form x, y'
        answer = raw_input()
        if isinstance(answer, str):
            answer = answer.split()
            answer[0] = answer[0].strip(',')
            A2 = disky.Disky((int(answer[0]), int(answer[1])))

    A2.run()
else:
    raise ValueError('Input must be integers of the form x, y')
