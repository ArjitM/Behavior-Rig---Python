# !/usr/bin/env/python3.6

import os
from randome import randint

def inputDigit(message):
    d = None
    while not d.isdigit():
        d = input(message)
    d = int(d)
    return d

def usePresets():
    preset = 0
    while preset not in range(1, 5):
        preset = input('Enter preset from nights 1-4 (exit to leave preset menu): ')

        if preset == 'exit':
            return False

        if preset.isdigit():
            preset = int(preset)
        else:
            print('Integers or "exit" only!')
            preset = 0

    if preset == 1:
        images_and_times = ['gray.png']
        times = [experiment_length]
        fixed_order = True
        reward_set = ['gray.png']
        off_img = None
        fixed_times = True

    elif preset == 2:
        images_and_times = {'gray.png': 60, 'vertical_bw.png': 60, 'horizontal_bw.png': 60}
        fixed_order = True
        reward_set = ['vertical_bw.png']
        off_img = 'black.png'
        off_time = 420
        fixed_times = True


    elif preset == 3:
        images_and_times = {'gray.png': 30, 'vertical_bw.png': 30, 'horizontal_bw.png': 30}
        fixed_order = False
        reward_set = ['vertical_bw.png']
        off_img = 'black.png'
        off_time = 120
        fixed_times = True

    else:
        min_duration = 12
        max_duration = 120
        images_and_times = {'gray.png': (min_duration, max_duration), 'vertical_bw.png': (min_duration, max_duration), 'horizontal_bw.png': (min_duration, max_duration)}
        fixed_order = False
        reward_set = ['vertical_bw']
        off_img = None
        fixed_times = False

    return preset


def getNewProtocol():
    directory = input('Enter directory where images are stored: ')
    if not directory.endswith('/'):
        directory += '/'

    fixed_times = input('Fixed times for images? (yes/no): ').lower().startswith('y')

    images_and_times = {}
    reward_set = []
    fixed_order = input('Fixed order? (yes/no): ').lower().startswith('y')

    if fixed_times:

        for f in next(os.walk(dir))[1]:
            if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.tif'):
                
                duration = inputDigit('Length of display for image {0}: '.format(f))

                img_type = input('What is this image? Control (c), Reward (r), Off (o), or Remove from list (x): ').lower()
                if img_type.startswith('o'):
                    off_img = (f, duration) 
                elif img_type.startswith('r'):
                    images_and_times[f] = duration
                    reward_set.append(f)
                elif img_type.startswith('c'):
                    images_and_times[f] = duration
                else:
                    pass

    else:

        for f in next(os.walk(dir))[1]:
            if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.tif'):

                def valid(duration):
                    if duration is None or type(duration) != tuple:
                        return False
                    i, j = duration
                    try:
                        i, j = int(i), int(j)
                    except ValueError:
                        return False
                    else:
                        return i <= j

                duration = None
                while not valid(duration):
                    duration = (inputDigit('Minimum length of display for image {0}: '.format(f)), inputDigit('Maximum length of display for image {0}: '.format(f)))

                img_type = input('What is this image? Control (c), Reward (r), Off (o), or Remove from list (x): ').lower()
                if img_type.startswith('o'):
                    off_img = f 
                    off_time = duration
                elif img_type.startswith('r'):
                    images_and_times[f] = duration
                    reward_set.append(f)
                elif img_type.startswith('c')
                    images_and_times[f] = duration
                else:
                    pass
    if off_img:
        if fixed_order:
            off_interperse = input('Should off image be at the end of cycle (e) or after each image (a)?: ').lower().startswith(a)
        else:
            off_spacing = inputDigit('Off image will be shown after every n (integer) images: ')


def generateFile(wheel_trigger, wheel_interval, reward_duration, metadata):
    sequence_imgs = []
    sequence_times = []
    total_time = 0
    images = list(images_and_times.keys())

    if fixed_order:

        k = 0

        while total_time < experiment_length:

            img = images[k % len(images)] # % allows for wrapping around the array
            k += 1
            duration = images_and_times[img]
            if type(duration) == tuple:
                duration = randint(duration[0], duration[1])

            sequence_imgs.append(img)
            sequence_times.append(duration)
            total_time += duration

            if total_time > experiment_length:
                break

            if off_img and (off_interperse or k % len(images) == 0):
                sequence_imgs.append(off_img)
                duration = off_time
                if type(duration) == tuple: #if time is variable, get random value within range
                    duration = randint(duration[0], duration[1])
                sequence_times.append(duration)
                total_time += duration



    else:

        k, previous = -1, -1
        count = 0

        while total_time < experiment_length:
            if off_img:
                k = randint(0, len(images) - 1)
                count += 1
            else: 
                while k != previous:
                    k = randint(0, len(images) - 1)
                previous = k

            img = images(k)
            time = images_and_times[img]
            if type(time) == tuple:
                time = randint(time[0], time[1])



        sequence.append(img)
        t = images_and_times[img]
        times.append(t)
        total_time += t
        if total_time < experiment_length:
            sequence.append(off_img)
            times.append(off_time)
            total_time += off_time


        with open('Protocol.txt', 'w') as pfile:
            pfile.write('image: [%s]' % ', '.join(map(str, cycle_imgs)))
            pfile.write('time: [%s]' % ', '.join(map(str, cycle_times)))
            pfile.write('reward: [%s]' % ', '.join(map(str, reward_set)))
            pfile.write('wheel trigger: {0}'.format(wheel_trigger))
            pfile.write('reward duration: {0}'.format(reward_duration))
            pfile.write('wheel interval: {0}'.format(wheel_interval))
            pfile.write('This is metadata............')
            pfile.write(metadata)
    


def main():
    global experiment_length
    global images
    global times
    global fixed_times
    global fixed_order
    global off_img
    off_img = None
    global off_time
    global reward_set
    global off_interperse #for use with fixed order
    global off_spacing #for use with no fixed order
    
    experiment_length = inputDigit("Enter experiment length in HOURS: ")
    experiment_length *= (60**2) #convert hours to seconds

    wheel_trigger = input('Wheel trigger (yes/no): ').lower().startswith('y')
    wheel_interval = inputDigit('Wheel interval (seconds): ')
    reward_duration = inputDigit('Duration of reward (seconds): ')
    metadata

    presets = input('Use preset protocol? (yes/no): ').lower().startswith('y') #use pre-defined protocols for nights 1-4
    loadedProtocol = False
    if presets:
        loadedProtocol = usePresets()
    if not loadedProtocol:
        getNewProtocol()

    generateFile(wheel_trigger, wheel_interval, reward_duration, metadata)



if __name__ == '__main__':
    main()

