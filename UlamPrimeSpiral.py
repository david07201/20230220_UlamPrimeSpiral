from tkinter import *
from tkinter import messagebox
import time

def for2and3(a):
    global x, y, DIRECTION, direction_factor, t
    for n in range(2, a+1):
        turn(n)
        x += DIRECTION[direction_factor][0]
        y += DIRECTION[direction_factor][1]
        #print(x, y)
        canvas.create_rectangle(x, y, x, y, width=0, fill='#FFFFFF')
        if animation.get() == True:
            canvas.update()
            time.sleep(t)

def turn(n,):
    global step, step_factor, total_step, direction_factor
    if n > total_step:
        total_step += step
        step += step_factor
        step_factor ^= 1
        direction_factor += 1
        direction_factor %= 4

def generate():
    global direction_factor, step, step_factor, total_step, x, y
    global root, frame, label3, t

    try:
        a = int(size.get())
    except:
        messagebox.showerror('數值錯誤', '請輸入正整數')
        return
    
    if animation.get() == True:
        f = int(frequency.get())
        if f <= 0:
            messagebox.showerror('FPS錯誤', '請輸入正整數')
            return
        if f > 100:
            messagebox.showerror('FPS錯誤', '請輸入 100 以下的正整數')
            return
        
        total_t = int(a / f * 1.5)
        msg = ''
        if total_t >= 3600:
            h = total_t // 3600
            total_t -= h * 3600
            msg += str(h) + ' 小時 '
        if total_t >= 60:
            m = total_t // 60
            s = total_t - m * 60
            msg += str(m) + ' 分 '
            if s > 0:
                msg += str(s) + ' 秒 '
        else:
            msg += str(total_t) + ' 秒 '    

        if messagebox.askokcancel(
            '預估耗時', f'預估耗時 {msg}，是否執行？') == False:
            return

        t = 1 / f

    t1 =time.perf_counter_ns()
    canvas.delete('all')
    direction_factor = -1
    step = 1
    step_factor = 0
    total_step = 1

    canvas_size = int(a**0.5) + 10
    if canvas_size & 1 == 0:
        canvas_size += 1
    canvas.configure(width=canvas_size, height=canvas_size)
    x, y = canvas_size//2 + 1, canvas_size//2 + 1
    #print(x, y)

    if 2 <= a <= 3:
        for2and3(a)

    elif a > 3:
        for2and3(3)
        for n in range(4, a+1):
            b = int(n**0.5) # n>=4 -> b>1
            for p in prime_list:
                if p <= b:
                    if n % p == 0:
                        turn(n)
                        x += DIRECTION[direction_factor][0]
                        y += DIRECTION[direction_factor][1]
                        break
                else:
                    #print(n)
                    prime_list.append(n)
                    turn(n)
                    x += DIRECTION[direction_factor][0]
                    y += DIRECTION[direction_factor][1]
                    #print(x, y)
                    canvas.create_rectangle(
                        x, y, x, y, width=0, fill='#FFFFFF')
                    break

            if animation.get() == True:
                canvas.update()
                time.sleep(t)

    #print(len(prime_list))
    t2 = time.perf_counter_ns()
    label3.config(text=f'生成時間：{(t2-t1)/1000000} ms')


# start
DIRECTION = ((1, 0), (0, -1), (-1, 0), (0, 1))
prime_list = [2, 3]

root =Tk()
root.title('Ulam Spiral')
root.configure(bg='#B0B0B0')

canvas = Canvas(root, bg='#000000', width=100, height=100)
canvas.pack()
frame = Frame(root, bg='#B0B0B0')
frame.pack()

label1 = Label(frame, text='請輸入正整數：', bg='#B0B0B0')
size = IntVar()
size.set(0)
entry1 = Entry(frame, textvariable=size, width=8, justify='right')

label2 = Label(frame, text='FPS：', bg='#B0B0B0')
frequency = IntVar()
frequency.set(100)
entry2 = Entry(frame, textvariable=frequency, width=4, justify='right')

animation = BooleanVar()
animation.set(True)
checkbutton = Checkbutton(
    frame, text='動畫效果', variable=animation, bg='#B0B0B0')

button = Button(frame, text='生成', bg='#B0B0B0', command=generate)

label3 = Label(frame, text='生成時間： ms', bg='#B0B0B0')

label1.pack(side='left', padx=5)
entry1.pack(side='left')
label2.pack(side='left', padx=5)
entry2.pack(side='left')
checkbutton.pack(side='left', padx=5)
button.pack(side='left', padx=5)
label3.pack(side='left', padx=5)

root.mainloop()