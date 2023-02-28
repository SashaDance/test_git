"""
SIR (Susceptible Infected Removed)
Removed = выздоровевшие + умершие
Предположения о нашей модели:
• выздоровевшие люди получают 100% иммунитет к болезни;
• все смерти были вызваны только инфекцией;
• численность популяции постоянна (нет рождений);
• каждый человек имеет одинаковый шанс стать зараженным и удаленным из рассмотрения.
_____изменение____1231323
"""
# PRIVET
from scipy.integrate import odeint  # function for ODE solving
from manim import *
from manim.utils.unit import Pixels

N = 100  # Популяций (100 %)
I0 = 0.001  # Изначальный процент зараженного населения
R0 = 0  # Изначальный процент населения, удаленного из рассмотрения
S0 = N - I0 - R0  # Изначальный процент восприимчивого населения
# Параметры
beta = 0.143  # Параметр инфекции
gamma = 0.1075  # Параметр удаления
# Время модели
t_days = 400


# Дифференциальное уравнение
def diff_e(y, t):
    S, I, R = y
    dS_dt = -beta * S * I / N
    dI_dt = beta * S * I / N - gamma * I
    dR_dt = gamma * I
    return dS_dt, dI_dt, dR_dt


# Изначальные данные
y0 = S0, I0, R0


# Созадние видео
class SirVisualisation(Scene):
    def construct(self):
        ax = Axes(x_range=(0, t_days, 50), y_range=(0, N + 10, N // 10), axis_config={"include_numbers": True})
        y_name = Text('Percent of Population').scale(0.3)
        y_name.shift(550 * Pixels * LEFT, 290 * Pixels * UP)
        x_name = Text('Days').scale(0.3)
        x_name.shift(580 * Pixels * RIGHT, 270 * Pixels * DOWN)
        s_curve = ax.plot(lambda x:
                          odeint(diff_e, y0, [1, x])[1][0], color=RED)  # Кривая восприимчивых
        i_curve = ax.plot(lambda x:
                          odeint(diff_e, y0, [1, x])[1][1], color=YELLOW)  # Кривая зараженных
        r_curve = ax.plot(lambda x:
                          odeint(diff_e, y0, [1, x])[1][2], color=ORANGE)  # Кривая удаленных
        # Текущие значения восприимчивого, зараженного и удаленного населений
        s_tracker = ValueTracker(0)
        s_number = DecimalNumber(s_tracker.get_value(), color=RED, num_decimal_places=0).scale(0.7)
        s_text = Text('S =', color=RED).scale(0.5)
        s_text.shift(-310 * Pixels * RIGHT, 320 * Pixels * UP)
        s_number.next_to(s_text, RIGHT)
        s_number.add_updater(lambda obj:
                             obj.set_value(odeint(diff_e, y0, [1, s_tracker.get_value()])[1][0]))
        i_tracker = ValueTracker(0)
        i_number = DecimalNumber(i_tracker.get_value(), color=YELLOW, num_decimal_places=0).scale(0.7)
        i_text = Text('I =', color=YELLOW).scale(0.5)
        i_text.next_to(s_text, DOWN)
        i_number.next_to(i_text, RIGHT)
        i_number.add_updater(lambda obj:
                             obj.set_value(odeint(diff_e, y0, [1, i_tracker.get_value()])[1][1]))
        r_tracker = ValueTracker(0)
        r_number = DecimalNumber(i_tracker.get_value(), color=ORANGE, num_decimal_places=0).scale(0.7)
        r_text = Text('R =', color=ORANGE).scale(0.5)
        r_text.next_to(i_text, DOWN)
        r_number.next_to(r_text, RIGHT)
        r_number.add_updater(lambda obj:
                             obj.set_value(odeint(diff_e, y0, [1, r_tracker.get_value()])[1][2]))
        # Добавление объектов на экран
        self.add(ax, s_number, s_text,
                 i_number, i_text,
                 r_number, r_text,
                 y_name, x_name)
        self.play(Create(s_curve), Create(i_curve), Create(r_curve),
                  s_tracker.animate.set_value(t_days),
                  i_tracker.animate.set_value(t_days),
                  r_tracker.animate.set_value(t_days),
                  run_time=30)
        self.wait(5)
