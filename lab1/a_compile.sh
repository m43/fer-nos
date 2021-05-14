echo "Compile a_entry"
gcc a_entry.c a.h -Wall -o out/a_entry
echo

echo "Compile a_semaphore"
gcc a_semaphore.c a.h -Wall -o out/a_semaphore
echo

echo "Compile a_car"
gcc a_car.c a.h -Wall -o out/a_car
echo