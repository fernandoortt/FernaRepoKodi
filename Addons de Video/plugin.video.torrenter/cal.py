# -*- coding: utf-8 -*-
def log(x):
    print x


x = 'abcd'
y = 'abcd/abcde'

print y[:len(x)]




#print '*******************************************'
#labels = ['Открыть', "Download via T-client", 'Скачать Торр-клиентом',
#          'Individual Tracker Options','Выбор Трекеров', 'Высокий Приоритет Файлам']
#
#for label in labels:
#    label = label.decode('utf-8')
#    if len(label)>10:
#        spaces = label.count(' ')
#        log('spaces='+str(spaces))
#        if spaces == 0:
#            words = [label[:10], label[11:]]
#            label = '%s-\r\n%s' % (words[0], words[1])
#        elif spaces == 1:
#            words = label.split(' ')
#            label = '%s\r\n%s' % (words[0], words[1])
#        elif spaces == 2:
#            words = label.split(' ')
#            if len(words[0]) <= len(words[2]):
#                words[0] = words[0] + ' ' + words[1]
#                words[1] = words[2]
#            else:
#                words[1] = words[1] + ' ' + words[2]
#            label = '%s\r\n%s' % (words[0], words[1])
#
#        log('*** %d ************** %d ***********' % (len(words[0]), len(words[1])))
#    log(label)


