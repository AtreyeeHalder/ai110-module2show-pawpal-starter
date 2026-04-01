# PawPal+ Project Reflection

## 1. System Design

Three core actions a user should be able to perform on PawPal+ are:
i. Update and view pet details
ii. Create a schedule for feeding
iii. Add and view vet appointments

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The classes I included are Pet, FoodSchedule, and VetAppointments.
i. Pet: This class is responsible for viewing details about a pet and updating them. The attributes are String name, int age, String gender, String animal, String breed. The methods are getter (e.g. getName()) and setter (e.g. setAge(int age)) methods for the attributes, getInfo() for displaying all information about the current pet, and eat(String time) for tracking when the pet is fed.

ii. FoodSchedule: This class is responsible for creating a schedule for feeding a pet and keeping track of when the pet eats. The attributes are Pet pet, List<String> feedingTimes. The methods are addFeedingTime(String time), removeFeedingTime(String time), getSchedule(), markFed(String time).

iii. Appointment: This class is responsible for tracking information about appointments. The attributes are String date, String address, String vetName, String reason. The methods are getter and setter methods for all attributes.

iv. VetAppointments: This class is responsible for adding and viewing vet appointments for a pet, and recording reasons for a visit. The attributes are Pet pet, List<Appointment> appointments. The methods are addAppointment(String date, String address, String vetName, String reason), viewAppointments(), removeAppointment(String date, String address, String vetName, String reason), getNextAppointment().

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, during implementation my design changed based on Claude Code suggestions. The change is adding and removing appointments by a unique ID as the key for accessing a specific appointment instead of using the four attributes associated with it (date, address, vetName, reason) which could have easily led to a potential logic bottleneck of misspelling any of these attributes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The most important constraint my scheduler considers is time because if pet care tasks are not done on time, it could lead to the pet being unhappy or having health problems. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

A tradeoff my scheduler makes is that the mark_task_complete method uses string matching on the task description instead of using a unique ID to mark the specific tasks as complete. This tradeoff is reasonable because it is easier for a user to input the task description instead of remembering a unique ID. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
