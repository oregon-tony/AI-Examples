import time

def count_to_billion():
    start_time = time.time()

    for i in range(1, 1000000001):
        pass  # The loop does nothing but iterate

    end_time = time.time()
    duration = end_time - start_time
    print(f"Counting from 1 to 1,000,000,000 took {duration:.2f} seconds.")


if __name__ == "__main__":
    count_to_billion()
  
