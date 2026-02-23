# Task 0: Check Available Audio Systems

import sounddevice as sd
print(sd.query_devices())

# Print your results here:
# > 0 MacBook Air Microphone, Core Audio (1 in, 0 out)
# < 1 MacBook Air Speakers, Core Audio (0 in, 2 out)