import FRC, FTC

def main():
    runningError = 0

    while (runningError < 3):
        FTCOrFRC = input("Calculating for FRC or FTC: ")
        if FTCOrFRC == "FRC":
            FRC.FRCOPR()
            break
        elif FTCOrFRC == "FTC":
            FTC.FTCOPR()
            break
        else:
            print("Please make sure you specify which game your are checking")
            runningError += 1

    if (runningError == 3):
        print("Wrong for too many times, exiting...")

main()