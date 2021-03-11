import time


class StopWatch:
    def __init__(self):
        self.start_time = None
        self.finish_time = None
        self.buff_count = 0
        self.buff_time = [time.time()]

    def start_stop_watch(self) -> float:
        self.start_time = time.time()
        print('--start stop watch--')

        return self.start_time

    def lap(self) -> list:
        self.buff_time.append(time.time())
        self.buff_count += 1

        diff_from_start_time = self.buff_time[self.buff_count] - self.start_time
        lap_time = self.buff_time[self.buff_count] - self.buff_time[self.buff_count - 1]
        print("lap {}  {}  +{}".format(self.buff_count, diff_from_start_time, lap_time))

        lap_list = [self.buff_count, diff_from_start_time, lap_time]

        return lap_list

    def finish_stop_watch(self) -> float:
        self.finish_time = time.time()
        print("--finish stop watch--")
        print("{}sec".format(self.finish_time - self.start_time))

        return self.finish_time


def main():
    pass


if __name__ == "__main__":
    main()
