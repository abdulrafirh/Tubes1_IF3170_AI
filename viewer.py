from manim import *

class DynamicNineCube(Scene):
    def construct(self):
        states = [
            [[1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24, 25, 26, 27]],
            [[1, 2, 3, 7, 5, 6, 4, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24, 25, 26, 27]],
            [[1, 2, 3, 7, 5, 6, 4, 8, 10], [9, 11, 12, 13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24, 25, 26, 27]],
            [[27, 2, 3, 7, 5, 6, 4, 8, 10], [9, 11, 12, 13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24, 25, 26, 1]],
        ]

        current_state_index = 0
        cubes = self.build_cubes(states[current_state_index])
        counter_text = Text(f"State {current_state_index}", font_size=36, color=WHITE)
        counter_text.to_edge(UP)
        
        self.add(cubes, counter_text)

        self.play(Rotate(cubes, angle=PI / 5, axis=UP, rate_func=linear, run_time=0.5))
        self.play(Rotate(cubes, angle=PI / 7, axis=RIGHT, rate_func=linear, run_time=0.5))

        for next_state_index in range(1, len(states)):
            current_state = states[current_state_index]
            next_state = states[next_state_index]

            new_counter_text = Text(f"State {next_state_index}", font_size=36, color=WHITE)
            new_counter_text.to_edge(UP)
            self.play(Transform(counter_text, new_counter_text),run_time=0.08)

            for x in range(9):
                for y in range(3):
                    if current_state[y][x] != next_state[y][x]:
                        cube_to_change = cubes[y * 9 + x]
                        original_color = cube_to_change[0].get_fill_color()

                        self.play(cube_to_change[0].animate.set_fill(YELLOW, opacity=1), run_time=0.05)

                        new_number = Text(str(next_state[y][x]), font_size=24, color=WHITE)
                        new_number.move_to(cube_to_change[0].get_center())
                        cube_to_change[1] = new_number
                        cube_to_change.add(new_number)
                        self.play(FadeIn(new_number, run_time=0.1))

                        self.play(cube_to_change[0].animate.set_fill(original_color, opacity=0.2),run_time=0.08)


            current_state_index = next_state_index

        self.wait(2)

    def build_cubes(self, state):
        cubes = VGroup()
        spacing = 1.6  

        for x in range(9):  
            for y in range(3):
                cube = Cube(side_length=0.5, fill_opacity=0.2, fill_color=BLUE)
                cube.shift(np.array([(x % 3 - 1) * spacing, (y - 1) * spacing, (x // 3 - 1) * spacing]))

                number = Text(str(state[y][x]), font_size=24, color=WHITE)
                number.move_to(cube.get_center())

                cube_with_number = VGroup(cube, number)
                cubes.add(cube_with_number)

        cubes.move_to(ORIGIN)
        return cubes
