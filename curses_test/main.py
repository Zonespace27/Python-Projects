import curses
import globals
import constants as const

# addstr: 1st is down, 2nd is across

def start_everything():
    curses.initscr()
    main_screen = curses.newwin(const.MAXIMUM_ROWS, const.MAXIMUM_COLUMNS, 0, 0)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    main_screen.refresh()

    globals.initialize(main_screen)



if __name__ == "__main__":
    try:
        start_everything()
    except:
        curses.nocbreak()
        curses.curs_set(True)
        curses.echo()
        curses.endwin() #fuck curses making me do this, can't use wrapper()
