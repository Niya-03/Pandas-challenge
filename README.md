**How to run the code**
To execute the code you should run the main.py file. If no errors occured the main function should print "Task finished successfully!". In case any method along the chain failed, it will print where the error occured and what it is exactly.

**How to run the tests**
To run the tests you should run the command "pytest" in the console from the root directory.

**Explanation of design decisions**
I have decided to turn every part of the task into a class with private methods and one public method that gets called in the main function. Every method returns True or False, depending on whether it finished its work successfully or not. I decided to implement it this way because if something fails along the way it can be traced very quickly. Also dividing it into classes and functions means in case of need for a change it is very easy to find the exact function where the change should occur.

Regarding data anomalies I have chosen to drop rows including invalid data. Specifically for products price I decided to do that because i think that if I fill it with 0.00 this will screw the reports later on and more data will become invalid or unusable.