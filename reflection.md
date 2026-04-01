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

I used Claude Code suggestions to brainstorm my UML design, draft code, and refactor logic to improve readability and make the code and README look professional. When I prompted Claude Code to make changes to the code, I asked it to give explanations for why it was making those specific changes before the changes were saved. Additionally, I used separate chat sessions for each specific feature to bring the AI's focus to one task at a time so it does not mix up solutions to many tasks. The most helpful prompts were the ones in which I specified and narrowed down the exact type of improvement I wanted, so the AI addressed those specifications.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When Claude Code suggestions initially drafted the code for the unique ID system in appointments, I noticed a gap in its logic: when an appointment is removed, the counter would skip that ID number the next time a new appointment is added. When I raised this concern to Claude Code, it suggested an alternative approach that correctly reuses ID gaps even if an appointment is removed. I verified this by looking through the suggested code before accepting it.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

i. Task completion: that calling `mark_complete()` on a task correctly flips its `completed` flag from `False` to `True`.
ii. Task addition: that adding a task to a pet increments the pet's task list as expected.
iii. Chronological sorting — that `get_all_tasks_sorted_by_time` returns tasks in true clock order (e.g., 8:00 AM before 1:00 PM before 6:00 PM), across multiple pets, and returns an empty list when no tasks exist.
iv. Recurrence logic: that completing a `daily` task auto-generates a new task due the next day, a `weekly` task generates one due in 7 days, and a `monthly` task is simply marked done with no new task created. I also tested that completing an already-finished task or a task belonging to an unknown pet is handled without errors.
v. Conflict detection: that `detect_conflicts` correctly identifies when two tasks share a time slot, returns exactly one warning per conflicting slot (naming both pets and the time), and returns an empty list when there are no overlaps.

These tests were important because the app may run without crashing while producing a plan that may lead to negative consequences, like two tasks assigned at the same time, or a recurring task never rescheduled.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident (4/5) that the core scheduling logic works correctly. The test suite covers the main happy paths and the most likely edge cases for each feature. An area of lower confidence is the Streamlit UI layer, which is only verified manually. If I had more time, I would test: tasks added with identical descriptions on the same pet (to verify string-matching behavior in `mark_task_complete`), schedules with a large number of tasks to check sorting performance, and the behavior of `detect_conflicts` when a single pet has two tasks at the same time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the recurrence logic because with the help of Claude Code, I was able to learn and implement a new concept about timedelta in Python which I found very interesting.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would expand conflict detection to time duration instead of checking for only the starting time of the tasks, since each task like walking or going to an appointment generally takes some time to complete, so checking for duration overlap is important.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that AI collaboration requires active judgment at every step. Claude Code accelerated the drafting and refactoring work significantly, but it also introduced subtle logic gaps that I was only able to notice when reading the code critically and thinking through edge cases. Thus, when collaborating with powerful AI tools, I learned that being the "lead architect" is neither about accepting AI-generated code blindly nor writing everything from scratch; it is about being the human-in-the-loop -- using AI to brainstorm, draft, and improve code efficiently while critiquing its actions at every step by evaluating tradeoffs and edge cases.
