import random
import time
from flask import Flask, render_template, request, Response, session
from flask_session import Session
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
import io
from utils.email_sender import send_email

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Replace with a secure key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Sample question bank (abbreviated for brevity; use your full version)
sample_questions = {
     "C": {
                "easy": [
                    {"question": "What is the output of printf(\"%d\", 5);?", "options": ["A. 5", "B. Error", "C. 0", "D. None"], "answer": "A", "explanation": "Prints 5."},
                    {"question": "Which keyword declares a variable?", "options": ["A. int", "B. var", "C. let", "D. const"], "answer": "A", "explanation": "int declares variables in C."},
                    {"question": "What is the size of int?", "options": ["A. 2 bytes", "B. 4 bytes", "C. 8 bytes", "D. Varies"], "answer": "B", "explanation": "Typically 4 bytes on most systems."},
                    {"question": "What does \\n do?", "options": ["A. New line", "B. Tab", "C. Space", "D. Null"], "answer": "A", "explanation": "Inserts a new line."},
                    {"question": "What is a pointer?", "options": ["A. Variable", "B. Address", "C. Function", "D. None"], "answer": "B", "explanation": "Stores memory address."},
                    {"question": "What is ++i?", "options": ["A. Increment", "B. Decrement", "C. Assign", "D. None"], "answer": "A", "explanation": "Increments i before use."},
                    {"question": "What is main()?", "options": ["A. Function", "B. Variable", "C. Class", "D. None"], "answer": "A", "explanation": "Entry point function."},
                    {"question": "What is #include?", "options": ["A. Directive", "B. Function", "C. Variable", "D. None"], "answer": "A", "explanation": "Preprocessor directive."},
                    {"question": "What is scanf()?", "options": ["A. Input", "B. Output", "C. Loop", "D. None"], "answer": "A", "explanation": "Reads input."},
                    {"question": "What is a char?", "options": ["A. Character", "B. Integer", "C. Float", "D. None"], "answer": "A", "explanation": "Stores a single character."}
                ],
                "intermediate": [
                    {"question": "What does *ptr mean?", "options": ["A. Pointer", "B. Value", "C. Address", "D. None"], "answer": "B", "explanation": "Dereferences pointer."},
                    {"question": "What is malloc()?", "options": ["A. Memory allocation", "B. Free memory", "C. Loop", "D. None"], "answer": "A", "explanation": "Allocates memory dynamically."},
                    {"question": "What is the purpose of free()?", "options": ["A. Allocate memory", "B. Deallocate memory", "C. Initialize memory", "D. None"], "answer": "B", "explanation": "Frees allocated memory."},
                    {"question": "What is a structure in C?", "options": ["A. Data type", "B. Function", "C. Variable", "D. None"], "answer": "A", "explanation": "User-defined data type."},
                    {"question": "What is the difference between == and =?", "options": ["A. Comparison vs Assignment", "B. Both are same", "C. None", "D. Error"], "answer": "A", "explanation": "== compares values, = assigns values."},
                    {"question": "What is a union?", "options": ["A. Data type", "B. Function", "C. Variable", "D. None"], "answer": "A", "explanation": "Stores different data types in the same memory location."},
                    {"question": "What is a static variable?", "options": ["A. Local variable", "B. Global variable", "C. Retains value", "D. None"], "answer": "C", "explanation": "Retains its value between function calls."},
                    {"question": "What is a header file?", "options": ["A. Contains declarations", "B. Contains definitions", "C. Both A and B", "D. None"], "answer": "C", "explanation": "Contains declarations and definitions."},
                    {"question": "What is a macro?", "options": ["A. Function-like construct", "B. Variable", "C. Data type", "D. None"], "answer": "A", "explanation": "A macro is a fragment of code that has been given a name."},
                    {"question": "What is the purpose of the 'const' keyword?", "options": ["A. Declare constant variable", "B. Declare variable", "C. Function", "D. None"], "answer": "A", "explanation": "Used to declare a variable whose value cannot be changed."}
                ],
                "high": [
                    {"question": "What is a segmentation fault?", "options": ["A. Memory error", "B. Syntax error", "C. Logic error", "D. None"], "answer": "A", "explanation": "Occurs when a program tries to access an area of memory that it is not allowed to."},
                    {"question": "What is the difference between stack and heap memory?", "options": ["A. Stack is static, heap is dynamic", "B. Both are same", "C. Stack is faster", "D. None"], "answer": "A", "explanation": "Stack memory is used for static memory allocation, while heap memory is used for dynamic memory allocation."},
                    {"question": "What is undefined behavior in C?", "options": ["A. Error", "B. No output", "C. Unexpected results", "D. None"], "answer": "C", "explanation": "Occurs when the code does something that the C standard does not define."},
                    {"question": "What is a race condition?", "options": ["A. Error", "B. Logic error", "C. Synchronization issue", "D. None"], "answer": "C", "explanation": "Occurs when two threads access shared data and try to change it at the same time."},
                    {"question": "What is the purpose of the 'volatile' keyword?", "options": ["A. Prevent optimization", "B. Declare variable", "C. Function", "D. None"], "answer": "A", "explanation": "Tells the compiler that the value of the variable may change at any time."},
                    {"question": "What is a dangling pointer?", "options": ["A. Points to invalid memory", "B. Points to valid memory", "C. Function", "D. None"], "answer": "A", "explanation": "A pointer that does not point to a valid object of the appropriate type."},
                    {"question": "What is the purpose of the 'extern' keyword?", "options": ["A. Declare variable", "B. Link variable", "C. Function", "D. None"], "answer": "B", "explanation": "Used to declare a variable that is defined in another file."},
                    {"question": "What is a function pointer?", "options": ["A. Pointer to a function", "B. Variable", "C. Data type", "D. None"], "answer": "A", "explanation": "A pointer that points to the address of a function."},
                    {"question": "What is the purpose of the 'sizeof' operator?", "options": ["A. Get size of variable", "B. Get size of function", "C. Get size of data type", "D. None"], "answer": "A", "explanation": "Returns the size of a variable or data type in bytes."},
                    {"question": "What is a memory leak?", "options": ["A. Memory not freed", "B. Memory freed", "C. Function", "D. None"], "answer": "A", "explanation": "Occurs when allocated memory is not freed."}
                ]
            },
            "Python": {
    "easy": [
        {"question": "What is the output of print(2 + 3)?", "options": ["A. 5", "B. 23", "C. Error", "D. None"], "answer": "A", "explanation": "Adds and prints 5."},
        {"question": "What is a list?", "options": ["A. Collection", "B. Function", "C. Class", "D. None"], "answer": "A", "explanation": "Ordered collection of items."},
        {"question": "What is len()?", "options": ["A. Length", "B. Loop", "C. Print", "D. None"], "answer": "A", "explanation": "Returns length of an object."},
        {"question": "What is 'if'?", "options": ["A. Conditional", "B. Loop", "C. Function", "D. None"], "answer": "A", "explanation": "Executes code conditionally."},
        {"question": "What is a string?", "options": ["A. Text", "B. Number", "C. Boolean", "D. None"], "answer": "A", "explanation": "Sequence of characters."},
        {"question": "What is range()?", "options": ["A. Sequence", "B. Function", "C. Class", "D. None"], "answer": "A", "explanation": "Generates sequence of numbers."},
        {"question": "What is None?", "options": ["A. Null", "B. Zero", "C. False", "D. None"], "answer": "A", "explanation": "Represents absence of value."},
        {"question": "What is input()?", "options": ["A. User input", "B. Output", "C. Loop", "D. None"], "answer": "A", "explanation": "Gets user input."},
        {"question": "What is a tuple?", "options": ["A. Immutable list", "B. Mutable list", "C. Function", "D. None"], "answer": "A", "explanation": "Immutable sequence."},
        {"question": "What does type(5) return?", "options": ["A. int", "B. float", "C. str", "D. bool"], "answer": "A", "explanation": "Returns the integer type."}
    ],
    "intermediate": [
        {"question": "What is a list comprehension?", "options": ["A. Loop shorthand", "B. Function", "C. Class", "D. None"], "answer": "A", "explanation": "Creates list in one line."},
        {"question": "What is lambda?", "options": ["A. Anonymous function", "B. Variable", "C. Loop", "D. None"], "answer": "A", "explanation": "Inline function definition."},
        {"question": "What does *args do?", "options": ["A. Variable arguments", "B. Keyword arguments", "C. Returns value", "D. None"], "answer": "A", "explanation": "Accepts variable number of arguments."},
        {"question": "What is __init__?", "options": ["A. Constructor", "B. Destructor", "C. Method", "D. Variable"], "answer": "A", "explanation": "Initializes class instances."},
        {"question": "What is a dictionary?", "options": ["A. Key-value pairs", "B. Ordered list", "C. Function", "D. None"], "answer": "A", "explanation": "Stores key-value mappings."},
        {"question": "What does 'with' statement do?", "options": ["A. File handling", "B. Loop", "C. Condition", "D. None"], "answer": "A", "explanation": "Manages resource cleanup."},
        {"question": "What is a set?", "options": ["A. Unique collection", "B. Ordered list", "C. Key-value pair", "D. None"], "answer": "A", "explanation": "Unordered unique elements."},
        {"question": "What does // operator do?", "options": ["A. Floor division", "B. Modulus", "C. Exponent", "D. None"], "answer": "A", "explanation": "Returns integer division result."},
        {"question": "What is a generator?", "options": ["A. Memory efficient", "B. Regular function", "C. Class", "D. None"], "answer": "A", "explanation": "Yields values one at a time."},
        {"question": "What does 'self' refer to?", "options": ["A. Instance", "B. Class", "C. Module", "D. None"], "answer": "A", "explanation": "Refers to the current instance."}
    ],
    "high": [
        {"question": "What is a decorator?", "options": ["A. Function modifier", "B. Variable", "C. Loop", "D. None"], "answer": "A", "explanation": "Modifies function behavior."},
        {"question": "What is metaclasses?", "options": ["A. Class of classes", "B. Regular class", "C. Function", "D. None"], "answer": "A", "explanation": "Defines class behavior."},
        {"question": "What is GIL?", "options": ["A. Global lock", "B. Local variable", "C. Function", "D. None"], "answer": "A", "explanation": "Global Interpreter Lock for threading."},
        {"question": "What is __slots__?", "options": ["A. Memory optimization", "B. Class method", "C. Variable", "D. None"], "answer": "A", "explanation": "Limits attribute creation."},
        {"question": "What is asyncio?", "options": ["A. Async programming", "B. Sync function", "C. Class", "D. None"], "answer": "A", "explanation": "Handles asynchronous operations."},
        {"question": "What is a context manager?", "options": ["A. Resource management", "B. Error handling", "C. Loop", "D. None"], "answer": "A", "explanation": "Manages resource lifecycle."},
        {"question": "What is monkey patching?", "options": ["A. Runtime modification", "B. Static code", "C. Function", "D. None"], "answer": "A", "explanation": "Modifies code at runtime."},
        {"question": "What is a descriptor?", "options": ["A. Attribute access", "B. Simple variable", "C. Loop", "D. None"], "answer": "A", "explanation": "Controls attribute behavior."},
        {"question": "What is pickling?", "options": ["A. Serialization", "B. Deserialization", "C. Function", "D. None"], "answer": "A", "explanation": "Converts objects to byte stream."},
        {"question": "What is a weak reference?", "options": ["A. Memory management", "B. Strong reference", "C. Variable", "D. None"], "answer": "A", "explanation": "Doesn't prevent garbage collection."}
    ]
},
           "C++": {
    "easy": [
        {"question": "What is cout?", "options": ["A. Output stream", "B. Input stream", "C. Variable", "D. None"], "answer": "A", "explanation": "Used to output data to console."},
        {"question": "What is the size of int?", "options": ["A. 4 bytes", "B. 2 bytes", "C. 8 bytes", "D. Varies"], "answer": "A", "explanation": "Typically 4 bytes on most systems."},
        {"question": "What does 'using namespace std;' do?", "options": ["A. Avoids std::", "B. Creates namespace", "C. Defines class", "D. None"], "answer": "A", "explanation": "Eliminates need for std:: prefix."},
        {"question": "What is a pointer?", "options": ["A. Memory address", "B. Value", "C. Function", "D. None"], "answer": "A", "explanation": "Stores memory address of a variable."},
        {"question": "What is 'cin' used for?", "options": ["A. Input", "B. Output", "C. Loop", "D. None"], "answer": "A", "explanation": "Reads input from console."},
        {"question": "What does 'int main()' define?", "options": ["A. Program entry", "B. Variable", "C. Class", "D. None"], "answer": "A", "explanation": "Main function where execution begins."},
        {"question": "What is '++' operator?", "options": ["A. Increment", "B. Decrement", "C. Assignment", "D. None"], "answer": "A", "explanation": "Increases value by 1."},
        {"question": "What is a reference?", "options": ["A. Alias", "B. Copy", "C. Pointer", "D. None"], "answer": "A", "explanation": "Alternative name for a variable."},
        {"question": "What does '#' symbol indicate?", "options": ["A. Preprocessor", "B. Comment", "C. Variable", "D. None"], "answer": "A", "explanation": "Indicates preprocessor directive."},
        {"question": "What is a class?", "options": ["A. Blueprint", "B. Function", "C. Variable", "D. None"], "answer": "A", "explanation": "Template for creating objects."}
    ],
    "intermediate": [
        {"question": "What is a constructor?", "options": ["A. Initializes object", "B. Destroys object", "C. Function", "D. None"], "answer": "A", "explanation": "Special method called when object is created."},
        {"question": "What is 'virtual' keyword?", "options": ["A. Polymorphism", "B. Encapsulation", "C. Variable", "D. None"], "answer": "A", "explanation": "Enables runtime polymorphism."},
        {"question": "What is operator overloading?", "options": ["A. Redefines operators", "B. Removes operators", "C. Creates operators", "D. None"], "answer": "A", "explanation": "Gives new meaning to operators."},
        {"question": "What is a destructor?", "options": ["A. Cleans up", "B. Creates object", "C. Copies object", "D. None"], "answer": "A", "explanation": "Called when object is destroyed."},
        {"question": "What is 'const' member function?", "options": ["A. Can't modify", "B. Can modify", "C. Static", "D. None"], "answer": "A", "explanation": "Cannot modify object state."},
        {"question": "What is a template?", "options": ["A. Generic programming", "B. Specific type", "C. Function", "D. None"], "answer": "A", "explanation": "Allows type-independent code."},
        {"question": "What does 'new' do?", "options": ["A. Allocates memory", "B. Frees memory", "C. Copies memory", "D. None"], "answer": "A", "explanation": "Dynamically allocates memory."},
        {"question": "What is 'delete' used for?", "options": ["A. Deallocates memory", "B. Allocates memory", "C. Copies memory", "D. None"], "answer": "A", "explanation": "Frees dynamically allocated memory."},
        {"question": "What is inheritance?", "options": ["A. Code reuse", "B. Encapsulation", "C. Overloading", "D. None"], "answer": "A", "explanation": "Class acquires properties of another."},
        {"question": "What is 'friend' keyword?", "options": ["A. Access control", "B. Type definition", "C. Variable", "D. None"], "answer": "A", "explanation": "Grants access to private members."}
    ],
    "high": [
        {"question": "What is RAII?", "options": ["A. Resource management", "B. Memory leak", "C. Function", "D. None"], "answer": "A", "explanation": "Resource Acquisition Is Initialization ties resources to object lifetime."},
        {"question": "What is a smart pointer?", "options": ["A. Auto-managed", "B. Manual pointer", "C. Variable", "D. None"], "answer": "A", "explanation": "Manages memory automatically."},
        {"question": "What is move semantics?", "options": ["A. Resource transfer", "B. Copy operation", "C. Delete operation", "D. None"], "answer": "A", "explanation": "Transfers ownership of resources."},
        {"question": "What is SFINAE?", "options": ["A. Template rule", "B. Syntax error", "C. Function", "D. None"], "answer": "A", "explanation": "Substitution Failure Is Not An Error for templates."},
        {"question": "What is a lambda expression?", "options": ["A. Anonymous function", "B. Named function", "C. Class", "D. None"], "answer": "A", "explanation": "Creates unnamed functions."},
        {"question": "What is exception safety?", "options": ["A. Error handling", "B. Memory leak", "C. Syntax", "D. None"], "answer": "A", "explanation": "Guarantees behavior during exceptions."},
        {"question": "What is a vtable?", "options": ["A. Virtual functions", "B. Static table", "C. Variable", "D. None"], "answer": "A", "explanation": "Table of virtual function pointers."},
        {"question": "What is CRTP?", "options": ["A. Static polymorphism", "B. Dynamic polymorphism", "C. Function", "D. None"], "answer": "A", "explanation": "Curiously Recurring Template Pattern."},
        {"question": "What is type erasure?", "options": ["A. Hides type", "B. Exposes type", "C. Deletes type", "D. None"], "answer": "A", "explanation": "Removes type information at runtime."},
        {"question": "What is constexpr?", "options": ["A. Compile-time", "B. Runtime", "C. Variable", "D. None"], "answer": "A", "explanation": "Evaluates expressions at compile time."}
    ]
},
            "Java": {
    "easy": [
        {"question": "What is the main method signature?", "options": ["A. public static void main(String[] args)", "B. void main()", "C. static main()", "D. None"], "answer": "A", "explanation": "Entry point for Java programs."},
        {"question": "What is System.out.println()?", "options": ["A. Prints output", "B. Reads input", "C. Creates object", "D. None"], "answer": "A", "explanation": "Outputs text to console."},
        {"question": "What is a class?", "options": ["A. Blueprint", "B. Function", "C. Variable", "D. None"], "answer": "A", "explanation": "Template for creating objects."},
        {"question": "What is 'int'?", "options": ["A. Integer type", "B. Float type", "C. String type", "D. None"], "answer": "A", "explanation": "Primitive type for whole numbers."},
        {"question": "What does 'public' mean?", "options": ["A. Accessible everywhere", "B. Private access", "C. Protected access", "D. None"], "answer": "A", "explanation": "Allows access from any class."},
        {"question": "What is a String?", "options": ["A. Text", "B. Number", "C. Boolean", "D. None"], "answer": "A", "explanation": "Sequence of characters."},
        {"question": "What is 'new' keyword?", "options": ["A. Creates object", "B. Deletes object", "C. Copies object", "D. None"], "answer": "A", "explanation": "Allocates memory for new object."},
        {"question": "What does '==' compare?", "options": ["A. Values", "B. References", "C. Types", "D. None"], "answer": "B", "explanation": "Compares object references."},
        {"question": "What is a package?", "options": ["A. Namespace", "B. Function", "C. Variable", "D. None"], "answer": "A", "explanation": "Groups related classes."},
        {"question": "What is 'void'?", "options": ["A. No return", "B. Returns value", "C. Class type", "D. None"], "answer": "A", "explanation": "Indicates no return value."}
    ],
    "intermediate": [
        {"question": "What is inheritance?", "options": ["A. Code reuse", "B. Encapsulation", "C. Overloading", "D. None"], "answer": "A", "explanation": "Class acquires properties of another."},
        {"question": "What is an interface?", "options": ["A. Contract", "B. Concrete class", "C. Variable", "D. None"], "answer": "A", "explanation": "Defines methods to implement."},
        {"question": "What is 'this' keyword?", "options": ["A. Current object", "B. Parent object", "C. New object", "D. None"], "answer": "A", "explanation": "Refers to current instance."},
        {"question": "What is a constructor?", "options": ["A. Initializes object", "B. Destroys object", "C. Copies object", "D. None"], "answer": "A", "explanation": "Special method for object creation."},
        {"question": "What is 'final' keyword?", "options": ["A. Constant", "B. Variable", "C. Mutable", "D. None"], "answer": "A", "explanation": "Prevents modification or overriding."},
        {"question": "What is polymorphism?", "options": ["A. Multiple forms", "B. Single form", "C. Encapsulation", "D. None"], "answer": "A", "explanation": "Objects can take multiple forms."},
        {"question": "What is 'static' keyword?", "options": ["A. Class level", "B. Instance level", "C. Local level", "D. None"], "answer": "A", "explanation": "Belongs to class, not instance."},
        {"question": "What is an ArrayList?", "options": ["A. Dynamic array", "B. Fixed array", "C. Function", "D. None"], "answer": "A", "explanation": "Resizable array implementation."},
        {"question": "What does 'throws' do?", "options": ["A. Declares exception", "B. Catches exception", "C. Creates exception", "D. None"], "answer": "A", "explanation": "Specifies method can throw exception."},
        {"question": "What is 'super' keyword?", "options": ["A. Parent class", "B. Current class", "C. Child class", "D. None"], "answer": "A", "explanation": "Refers to superclass."}
    ],
    "high": [
        {"question": "What is JVM?", "options": ["A. Virtual Machine", "B. Compiler", "C. Interpreter", "D. None"], "answer": "A", "explanation": "Java Virtual Machine executes bytecode."},
        {"question": "What is garbage collection?", "options": ["A. Memory cleanup", "B. Memory allocation", "C. Variable creation", "D. None"], "answer": "A", "explanation": "Automatically frees unused memory."},
        {"question": "What is a lambda expression?", "options": ["A. Anonymous function", "B. Named function", "C. Class", "D. None"], "answer": "A", "explanation": "Concise function definition."},
        {"question": "What is synchronization?", "options": ["A. Thread safety", "B. Thread creation", "C. Thread deletion", "D. None"], "answer": "A", "explanation": "Controls concurrent access."},
        {"question": "What is a generic type?", "options": ["A. Type safety", "B. Type casting", "C. Type conversion", "D. None"], "answer": "A", "explanation": "Parameterized types for flexibility."},
        {"question": "What is reflection?", "options": ["A. Runtime inspection", "B. Compile-time check", "C. Syntax check", "D. None"], "answer": "A", "explanation": "Examines class structure at runtime."},
        {"question": "What is a stream?", "options": ["A. Data processing", "B. File handling", "C. Thread", "D. None"], "answer": "A", "explanation": "Processes sequences of elements."},
        {"question": "What is JNI?", "options": ["A. Native interface", "B. Java interpreter", "C. Class loader", "D. None"], "answer": "A", "explanation": "Java Native Interface for native code."},
        {"question": "What is a volatile variable?", "options": ["A. Thread visibility", "B. Constant value", "C. Static value", "D. None"], "answer": "A", "explanation": "Ensures visibility across threads."},
        {"question": "What is dependency injection?", "options": ["A. Object provision", "B. Object creation", "C. Object deletion", "D. None"], "answer": "A", "explanation": "Provides dependencies to objects."}
    ]
},
            "Go": {
    "easy": [
        {"question": "What is the main package?", "options": ["A. Entry point", "B. Library", "C. Variable", "D. None"], "answer": "A", "explanation": "Defines program starting point."},
        {"question": "What does 'fmt.Println()' do?", "options": ["A. Prints output", "B. Reads input", "C. Creates file", "D. None"], "answer": "A", "explanation": "Prints to console."},
        {"question": "What is a 'var' keyword?", "options": ["A. Declares variable", "B. Defines function", "C. Creates type", "D. None"], "answer": "A", "explanation": "Declares a variable."},
        {"question": "What is 'int'?", "options": ["A. Integer type", "B. Float type", "C. String type", "D. None"], "answer": "A", "explanation": "Type for whole numbers."},
        {"question": "What does ':=' do?", "options": ["A. Short declaration", "B. Assignment", "C. Comparison", "D. None"], "answer": "A", "explanation": "Declares and assigns in one step."},
        {"question": "What is a slice?", "options": ["A. Dynamic array", "B. Fixed array", "C. Function", "D. None"], "answer": "A", "explanation": "Resizable view of an array."},
        {"question": "What is 'func' keyword?", "options": ["A. Defines function", "B. Defines variable", "C. Creates type", "D. None"], "answer": "A", "explanation": "Declares a function."},
        {"question": "What does 'package' keyword do?", "options": ["A. Groups code", "B. Imports code", "C. Exports code", "D. None"], "answer": "A", "explanation": "Organizes related code."},
        {"question": "What is 'bool' type?", "options": ["A. True/False", "B. Number", "C. String", "D. None"], "answer": "A", "explanation": "Represents boolean values."},
        {"question": "What does 'import' do?", "options": ["A. Uses external code", "B. Exports code", "C. Defines type", "D. None"], "answer": "A", "explanation": "Includes external packages."}
    ],
    "intermediate": [
        {"question": "What is a struct?", "options": ["A. Custom type", "B. Function", "C. Variable", "D. None"], "answer": "A", "explanation": "Groups fields into a type."},
        {"question": "What is an interface?", "options": ["A. Method set", "B. Concrete type", "C. Variable", "D. None"], "answer": "A", "explanation": "Defines behavior via methods."},
        {"question": "What does 'defer' do?", "options": ["A. Delays execution", "B. Executes immediately", "C. Defines type", "D. None"], "answer": "A", "explanation": "Schedules function to run later."},
        {"question": "What is a goroutine?", "options": ["A. Lightweight thread", "B. Main thread", "C. Function", "D. None"], "answer": "A", "explanation": "Concurrent function execution."},
        {"question": "What is a pointer?", "options": ["A. Memory address", "B. Value copy", "C. Type", "D. None"], "answer": "A", "explanation": "Holds address of a variable."},
        {"question": "What does 'make()' do?", "options": ["A. Initializes types", "B. Declares variable", "C. Copies value", "D. None"], "answer": "A", "explanation": "Creates slices, maps, channels."},
        {"question": "What is a map?", "options": ["A. Key-value store", "B. Ordered list", "C. Function", "D. None"], "answer": "A", "explanation": "Unordered key-value pairs."},
        {"question": "What does 'range' do?", "options": ["A. Iterates", "B. Declares", "C. Assigns", "D. None"], "answer": "A", "explanation": "Loops over slices, maps, etc."},
        {"question": "What is 'go' keyword?", "options": ["A. Starts goroutine", "B. Stops execution", "C. Defines type", "D. None"], "answer": "A", "explanation": "Launches concurrent execution."},
        {"question": "What is a method?", "options": ["A. Function with receiver", "B. Regular function", "C. Variable", "D. None"], "answer": "A", "explanation": "Function tied to a type."}
    ],
    "high": [
        {"question": "What is a channel?", "options": ["A. Communication pipe", "B. Data store", "C. Function", "D. None"], "answer": "A", "explanation": "Synchronizes goroutines."},
        {"question": "What is 'select' statement?", "options": ["A. Channel multiplexing", "B. Loop control", "C. Type switch", "D. None"], "answer": "A", "explanation": "Handles multiple channels."},
        {"question": "What is concurrency in Go?", "options": ["A. Goroutines + channels", "B. Threads only", "C. Processes", "D. None"], "answer": "A", "explanation": "Manages tasks via goroutines."},
        {"question": "What is a mutex?", "options": ["A. Synchronization", "B. Data type", "C. Function", "D. None"], "answer": "A", "explanation": "Locks shared resources."},
        {"question": "What is 'context' package?", "options": ["A. Request scoping", "B. Data storage", "C. Type definition", "D. None"], "answer": "A", "explanation": "Manages deadlines and cancellation."},
        {"question": "What is a race condition?", "options": ["A. Data conflict", "B. Syntax error", "C. Type error", "D. None"], "answer": "A", "explanation": "Uncontrolled concurrent access."},
        {"question": "What is 'iota'?", "options": ["A. Enum generator", "B. Loop counter", "C. Variable", "D. None"], "answer": "A", "explanation": "Auto-increments constants."},
        {"question": "What is 'runtime' package?", "options": ["A. System interaction", "B. File handling", "C. Type casting", "D. None"], "answer": "A", "explanation": "Controls runtime environment."},
        {"question": "What is a panic?", "options": ["A. Runtime error", "B. Syntax error", "C. Warning", "D. None"], "answer": "A", "explanation": "Stops execution on error."},
        {"question": "What is 'recover()'?", "options": ["A. Handles panic", "B. Creates error", "C. Loops", "D. None"], "answer": "A", "explanation": "Regains control after panic."}
    ]
},
            "React": {
    "easy": [
        {"question": "What is React?", "options": ["A. UI library", "B. Backend framework", "C. Database", "D. None"], "answer": "A", "explanation": "JavaScript library for building user interfaces."},
        {"question": "What is JSX?", "options": ["A. Syntax extension", "B. CSS framework", "C. Database query", "D. None"], "answer": "A", "explanation": "Allows HTML-like code in JavaScript."},
        {"question": "What is a component?", "options": ["A. Reusable UI", "B. Server function", "C. Data type", "D. None"], "answer": "A", "explanation": "Building block of React UI."},
        {"question": "What does 'props' stand for?", "options": ["A. Properties", "B. Procedures", "C. Protocols", "D. None"], "answer": "A", "explanation": "Data passed to components."},
        {"question": "What is the virtual DOM?", "options": ["A. Memory representation", "B. Real DOM", "C. Database", "D. None"], "answer": "A", "explanation": "Lightweight copy of actual DOM."},
        {"question": "What is 'state'?", "options": ["A. Component data", "B. Static data", "C. Server data", "D. None"], "answer": "A", "explanation": "Mutable data managed by component."},
        {"question": "What does 'render()' do?", "options": ["A. Displays UI", "B. Fetches data", "C. Deletes component", "D. None"], "answer": "A", "explanation": "Returns JSX to display."},
        {"question": "What is a functional component?", "options": ["A. JS function", "B. Class", "C. Module", "D. None"], "answer": "A", "explanation": "Function returning JSX."},
        {"question": "What is 'import React' for?", "options": ["A. Library access", "B. CSS styling", "C. Data fetch", "D. None"], "answer": "A", "explanation": "Imports React library."},
        {"question": "What is an event handler?", "options": ["A. User interaction", "B. Data storage", "C. Component type", "D. None"], "answer": "A", "explanation": "Handles user actions like clicks."}
    ],
    "intermediate": [
        {"question": "What are hooks?", "options": ["A. State in functions", "B. Class methods", "C. CSS hooks", "D. None"], "answer": "A", "explanation": "Add state to functional components."},
        {"question": "What is useState?", "options": ["A. Manages state", "B. Fetches data", "C. Renders UI", "D. None"], "answer": "A", "explanation": "Hook for state in functional components."},
        {"question": "What is useEffect?", "options": ["A. Side effects", "B. State reset", "C. Props update", "D. None"], "answer": "A", "explanation": "Handles side effects like data fetching."},
        {"question": "What is prop drilling?", "options": ["A. Passing props", "B. Component deletion", "C. State reset", "D. None"], "answer": "A", "explanation": "Passing props through multiple levels."},
        {"question": "What is a controlled component?", "options": ["A. Form with state", "B. Uncontrolled form", "C. Static UI", "D. None"], "answer": "A", "explanation": "Form data managed by React state."},
        {"question": "What is React Router?", "options": ["A. Navigation", "B. State management", "C. Data fetching", "D. None"], "answer": "A", "explanation": "Handles routing in React apps."},
        {"question": "What is a key prop?", "options": ["A. List identifier", "B. State variable", "C. Function name", "D. None"], "answer": "A", "explanation": "Uniquely identifies list items."},
        {"question": "What is component lifecycle?", "options": ["A. Mount/update/unmount", "B. Render only", "C. Props only", "D. None"], "answer": "A", "explanation": "Phases of component existence."},
        {"question": "What is conditional rendering?", "options": ["A. Dynamic UI", "B. Static UI", "C. Data fetch", "D. None"], "answer": "A", "explanation": "Renders based on conditions."},
        {"question": "What is a fragment?", "options": ["A. Groups elements", "B. Single element", "C. CSS class", "D. None"], "answer": "A", "explanation": "Wraps multiple elements without div."}
    ],
    "high": [
        {"question": "What is Context API?", "options": ["A. Global state", "B. Local state", "C. CSS context", "D. None"], "answer": "A", "explanation": "Shares data without prop drilling."},
        {"question": "What is Redux?", "options": ["A. State management", "B. Routing", "C. Data fetching", "D. None"], "answer": "A", "explanation": "Predictable state container."},
        {"question": "What is memoization in React?", "options": ["A. Performance boost", "B. State reset", "C. Props change", "D. None"], "answer": "A", "explanation": "Caches results to avoid re-renders."},
        {"question": "What is useCallback?", "options": ["A. Memoizes functions", "B. Memoizes state", "C. Renders UI", "D. None"], "answer": "A", "explanation": "Prevents function re-creation."},
        {"question": "What is useMemo?", "options": ["A. Memoizes values", "B. Updates state", "C. Fetches data", "D. None"], "answer": "A", "explanation": "Caches computed values."},
        {"question": "What is lazy loading?", "options": ["A. Delayed loading", "B. Immediate loading", "C. State loading", "D. None"], "answer": "A", "explanation": "Loads components on demand."},
        {"question": "What is React Suspense?", "options": ["A. Async rendering", "B. Sync rendering", "C. Error handling", "D. None"], "answer": "A", "explanation": "Handles asynchronous operations."},
        {"question": "What is a higher-order component?", "options": ["A. Enhances component", "B. Basic component", "C. CSS component", "D. None"], "answer": "A", "explanation": "Function that returns enhanced component."},
        {"question": "What is error boundary?", "options": ["A. Catches errors", "B. Creates errors", "C. Ignores errors", "D. None"], "answer": "A", "explanation": "Handles JavaScript errors in components."},
        {"question": "What is reconciliation?", "options": ["A. DOM diffing", "B. State merging", "C. Props copying", "D. None"], "answer": "A", "explanation": "Process of updating the DOM efficiently."}
    ]
},
            "HTML": {
    "easy": [
        {"question": "What does HTML stand for?", "options": ["A. HyperText Markup Language", "B. HighText Machine Language", "C. HyperTool Markup Language", "D. None"], "answer": "A", "explanation": "HTML is a markup language for web pages."},
        {"question": "What is the purpose of the <html> tag?", "options": ["A. Root element", "B. Paragraph", "C. Heading", "D. None"], "answer": "A", "explanation": "Defines the root of an HTML document."},
        {"question": "What does <body> contain?", "options": ["A. Visible content", "B. Metadata", "C. Scripts", "D. None"], "answer": "A", "explanation": "Holds content visible to users."},
        {"question": "What is an <h1> tag?", "options": ["A. Heading", "B. Paragraph", "C. Link", "D. None"], "answer": "A", "explanation": "Defines the largest heading."},
        {"question": "What does <a> tag do?", "options": ["A. Creates a link", "B. Adds an image", "C. Defines a list", "D. None"], "answer": "A", "explanation": "Creates hyperlinks."},
        {"question": "What is the role of <img> tag?", "options": ["A. Embeds images", "B. Creates text", "C. Adds styles", "D. None"], "answer": "A", "explanation": "Displays images on the page."},
        {"question": "What does <p> stand for?", "options": ["A. Paragraph", "B. Page", "C. Picture", "D. None"], "answer": "A", "explanation": "Defines a paragraph of text."},
        {"question": "What is the <br> tag for?", "options": ["A. Line break", "B. Bold text", "C. Blockquote", "D. None"], "answer": "A", "explanation": "Inserts a single line break."},
        {"question": "What does <ul> create?", "options": ["A. Unordered list", "B. Ordered list", "C. Table", "D. None"], "answer": "A", "explanation": "Creates a bulleted list."},
        {"question": "What is the <div> tag?", "options": ["A. Container", "B. Image", "C. Link", "D. None"], "answer": "A", "explanation": "Block-level container for content."}
    ],
    "intermediate": [
        {"question": "What is the <form> tag for?", "options": ["A. User input", "B. Styling", "C. Scripting", "D. None"], "answer": "A", "explanation": "Creates a form for user input."},
        {"question": "What does 'id' attribute do?", "options": ["A. Unique identifier", "B. Class name", "C. Style rule", "D. None"], "answer": "A", "explanation": "Provides a unique ID to an element."},
        {"question": "What is the <input> tag used for?", "options": ["A. Form fields", "B. Paragraphs", "C. Headings", "D. None"], "answer": "A", "explanation": "Creates input fields in forms."},
        {"question": "What does <meta> tag do?", "options": ["A. Metadata", "B. Content", "C. Links", "D. None"], "answer": "A", "explanation": "Provides metadata about the document."},
        {"question": "What is semantic HTML?", "options": ["A. Meaningful tags", "B. Random tags", "C. Style tags", "D. None"], "answer": "A", "explanation": "Uses tags that convey meaning."},
        {"question": "What does <table> create?", "options": ["A. Data grid", "B. List", "C. Form", "D. None"], "answer": "A", "explanation": "Defines a table structure."},
        {"question": "What is the 'class' attribute?", "options": ["A. Groups elements", "B. Unique ID", "C. Inline style", "D. None"], "answer": "A", "explanation": "Assigns a class for styling or scripting."},
        {"question": "What does <head> contain?", "options": ["A. Metadata", "B. Visible content", "C. Body", "D. None"], "answer": "A", "explanation": "Holds metadata and document info."},
        {"question": "What is the <iframe> tag?", "options": ["A. Embedded content", "B. Image", "C. List", "D. None"], "answer": "A", "explanation": "Embeds another HTML page."},
        {"question": "What does 'alt' attribute do?", "options": ["A. Image description", "B. Link text", "C. Style rule", "D. None"], "answer": "A", "explanation": "Provides alternative text for images."}
    ],
    "high": [
        {"question": "What is HTML5?", "options": ["A. Latest standard", "B. Old version", "C. CSS version", "D. None"], "answer": "A", "explanation": "Modern version with new features."},
        {"question": "What is the <canvas> tag?", "options": ["A. Graphics drawing", "B. Text display", "C. Form input", "D. None"], "answer": "A", "explanation": "Used for drawing graphics via JavaScript."},
        {"question": "What does <section> represent?", "options": ["A. Thematic content", "B. Random block", "C. Style block", "D. None"], "answer": "A", "explanation": "Groups related content."},
        {"question": "What is the <article> tag?", "options": ["A. Independent content", "B. Dependent content", "C. Script", "D. None"], "answer": "A", "explanation": "Self-contained content."},
        {"question": "What does <audio> do?", "options": ["A. Embeds sound", "B. Displays text", "C. Creates form", "D. None"], "answer": "A", "explanation": "Adds audio content."},
        {"question": "What is the <video> tag for?", "options": ["A. Video playback", "B. Image display", "C. List creation", "D. None"], "answer": "A", "explanation": "Embeds video content."},
        {"question": "What is 'data-' attribute?", "options": ["A. Custom data", "B. Style data", "C. Link data", "D. None"], "answer": "A", "explanation": "Stores custom data attributes."},
        {"question": "What does <nav> represent?", "options": ["A. Navigation links", "B. Content block", "C. Form", "D. None"], "answer": "A", "explanation": "Section for navigation links."},
        {"question": "What is ARIA?", "options": ["A. Accessibility", "B. Styling", "C. Animation", "D. None"], "answer": "A", "explanation": "Enhances accessibility for users."},
        {"question": "What is microdata?", "options": ["A. Structured data", "B. Random data", "C. Style data", "D. None"], "answer": "A", "explanation": "Adds machine-readable data."}
    ]
},
             "CSS": {
    "easy": [
        {"question": "What does CSS stand for?", "options": ["A. Cascading Style Sheets", "B. Computer Style System", "C. Creative Style Syntax", "D. None"], "answer": "A", "explanation": "Styles HTML elements."},
        {"question": "What is a selector?", "options": ["A. Targets elements", "B. Creates elements", "C. Deletes elements", "D. None"], "answer": "A", "explanation": "Selects HTML elements to style."},
        {"question": "What does 'color' property do?", "options": ["A. Sets text color", "B. Sets background", "C. Sets border", "D. None"], "answer": "A", "explanation": "Defines text color."},
        {"question": "What is the 'background' property?", "options": ["A. Sets background", "B. Sets text", "C. Sets margin", "D. None"], "answer": "A", "explanation": "Styles element background."},
        {"question": "What does 'font-size' control?", "options": ["A. Text size", "B. Line height", "C. Border size", "D. None"], "answer": "A", "explanation": "Sets the size of text."},
        {"question": "What is a class selector?", "options": ["A. .class", "B. #id", "C. element", "D. None"], "answer": "A", "explanation": "Targets elements with a class."},
        {"question": "What does 'margin' do?", "options": ["A. Outer space", "B. Inner space", "C. Border size", "D. None"], "answer": "A", "explanation": "Space outside an element."},
        {"question": "What is 'padding'?", "options": ["A. Inner space", "B. Outer space", "C. Text color", "D. None"], "answer": "A", "explanation": "Space inside an element."},
        {"question": "What does 'display: block' do?", "options": ["A. Full width", "B. Inline element", "C. Hidden", "D. None"], "answer": "A", "explanation": "Makes element a block."},
        {"question": "What is an ID selector?", "options": ["A. #id", "B. .class", "C. element", "D. None"], "answer": "A", "explanation": "Targets a unique element."}
    ],
    "intermediate": [
        {"question": "What is 'position: absolute'?", "options": ["A. Relative to parent", "B. Fixed position", "C. Normal flow", "D. None"], "answer": "A", "explanation": "Positioned relative to nearest positioned ancestor."},
        {"question": "What does 'flex' do?", "options": ["A. Flexible layout", "B. Grid layout", "C. Fixed layout", "D. None"], "answer": "A", "explanation": "Enables flexible box layout."},
        {"question": "What is a pseudo-class?", "options": ["A. Dynamic state", "B. Static class", "C. Element type", "D. None"], "answer": "A", "explanation": "Styles elements in specific states."},
        {"question": "What does 'z-index' control?", "options": ["A. Stacking order", "B. Font size", "C. Margin", "D. None"], "answer": "A", "explanation": "Determines element layering."},
        {"question": "What is 'box-sizing'?", "options": ["A. Size calculation", "B. Color scheme", "C. Font style", "D. None"], "answer": "A", "explanation": "Defines how box size is calculated."},
        {"question": "What does 'overflow' do?", "options": ["A. Content clipping", "B. Text alignment", "C. Border style", "D. None"], "answer": "A", "explanation": "Handles content overflow."},
        {"question": "What is a media query?", "options": ["A. Responsive design", "B. Static style", "C. Animation", "D. None"], "answer": "A", "explanation": "Applies styles based on conditions."},
        {"question": "What does 'float' do?", "options": ["A. Moves element", "B. Centers element", "C. Hides element", "D. None"], "answer": "A", "explanation": "Floats element left or right."},
        {"question": "What is 'display: none'?", "options": ["A. Hides element", "B. Shows element", "C. Blocks element", "D. None"], "answer": "A", "explanation": "Removes element from layout."},
        {"question": "What is a CSS variable?", "options": ["A. Reusable value", "B. Fixed value", "C. Class name", "D. None"], "answer": "A", "explanation": "Stores reusable values."}
    ],
    "high": [
        {"question": "What is CSS Grid?", "options": ["A. 2D layout", "B. 1D layout", "C. Float layout", "D. None"], "answer": "A", "explanation": "Two-dimensional layout system."},
        {"question": "What is a CSS preprocessor?", "options": ["A. Extends CSS", "B. Minifies CSS", "C. Replaces CSS", "D. None"], "answer": "A", "explanation": "Adds features like variables."},
        {"question": "What does 'transform' do?", "options": ["A. Modifies shape", "B. Changes color", "C. Adjusts font", "D. None"], "answer": "A", "explanation": "Applies 2D/3D transformations."},
        {"question": "What is 'transition'?", "options": ["A. Smooth change", "B. Static style", "C. Layout shift", "D. None"], "answer": "A", "explanation": "Animates property changes."},
        {"question": "What is '@keyframes'?", "options": ["A. Defines animation", "B. Sets color", "C. Adjusts margin", "D. None"], "answer": "A", "explanation": "Specifies animation steps."},
        {"question": "What does 'calc()' do?", "options": ["A. Computes values", "B. Sets static size", "C. Defines color", "D. None"], "answer": "A", "explanation": "Performs calculations in CSS."},
        {"question": "What is specificity?", "options": ["A. Rule priority", "B. Style order", "C. Font weight", "D. None"], "answer": "A", "explanation": "Determines which style applies."},
        {"question": "What is a pseudo-element?", "options": ["A. Styles parts", "B. Styles classes", "C. Styles tags", "D. None"], "answer": "A", "explanation": "Targets specific parts of elements."},
        {"question": "What does 'vh' unit mean?", "options": ["A. Viewport height", "B. Fixed height", "C. Pixel height", "D. None"], "answer": "A", "explanation": "Relative to viewport height."},
        {"question": "What is 'will-change'?", "options": ["A. Performance hint", "B. Style reset", "C. Color change", "D. None"], "answer": "A", "explanation": "Optimizes upcoming changes."}
    ]
},
            "JS": {
    "easy": [
        {"question": "What is JavaScript?", "options": ["A. Scripting language", "B. Markup language", "C. Styling language", "D. None"], "answer": "A", "explanation": "Used for web interactivity."},
        {"question": "What does 'console.log()' do?", "options": ["A. Prints to console", "B. Creates variable", "C. Defines function", "D. None"], "answer": "A", "explanation": "Outputs messages to console."},
        {"question": "What is a variable?", "options": ["A. Data container", "B. Function", "C. Class", "D. None"], "answer": "A", "explanation": "Stores data values."},
        {"question": "What does 'let' do?", "options": ["A. Declares variable", "B. Defines constant", "C. Creates loop", "D. None"], "answer": "A", "explanation": "Declares block-scoped variable."},
        {"question": "What is an array?", "options": ["A. Ordered list", "B. Key-value pair", "C. Function", "D. None"], "answer": "A", "explanation": "Stores multiple values."},
        {"question": "What does 'if' statement do?", "options": ["A. Conditional logic", "B. Loops", "C. Defines function", "D. None"], "answer": "A", "explanation": "Executes code based on condition."},
        {"question": "What is a function?", "options": ["A. Reusable code", "B. Variable", "C. Class", "D. None"], "answer": "A", "explanation": "Block of reusable code."},
        {"question": "What does '===' mean?", "options": ["A. Strict equality", "B. Loose equality", "C. Assignment", "D. None"], "answer": "A", "explanation": "Checks value and type."},
        {"question": "What is 'document'?", "options": ["A. DOM access", "B. File system", "C. Console", "D. None"], "answer": "A", "explanation": "Represents the webpage."},
        {"question": "What does 'addEventListener' do?", "options": ["A. Handles events", "B. Creates variables", "C. Defines styles", "D. None"], "answer": "A", "explanation": "Listens for user actions."}
    ],
    "intermediate": [
        {"question": "What is a closure?", "options": ["A. Function scope", "B. Global variable", "C. Class", "D. None"], "answer": "A", "explanation": "Function with access to outer scope."},
        {"question": "What does 'this' refer to?", "options": ["A. Current context", "B. Global object", "C. Function", "D. None"], "answer": "A", "explanation": "Depends on how function is called."},
        {"question": "What is a promise?", "options": ["A. Async result", "B. Sync result", "C. Variable", "D. None"], "answer": "A", "explanation": "Represents future value."},
        {"question": "What does 'async' do?", "options": ["A. Enables await", "B. Blocks code", "C. Defines loop", "D. None"], "answer": "A", "explanation": "Marks function as asynchronous."},
        {"question": "What is 'map()' method?", "options": ["A. Transforms array", "B. Filters array", "C. Reduces array", "D. None"], "answer": "A", "explanation": "Creates new array from results."},
        {"question": "What is an object?", "options": ["A. Key-value pairs", "B. Ordered list", "C. Function", "D. None"], "answer": "A", "explanation": "Collection of properties."},
        {"question": "What does 'try/catch' do?", "options": ["A. Error handling", "B. Loops", "C. Conditions", "D. None"], "answer": "A", "explanation": "Handles exceptions."},
        {"question": "What is 'setTimeout'?", "options": ["A. Delays execution", "B. Immediate execution", "C. Loops", "D. None"], "answer": "A", "explanation": "Executes after a delay."},
        {"question": "What is a callback?", "options": ["A. Function argument", "B. Variable", "C. Class", "D. None"], "answer": "A", "explanation": "Function passed as an argument."},
        {"question": "What does 'filter()' do?", "options": ["A. Selects elements", "B. Maps elements", "C. Reduces elements", "D. None"], "answer": "A", "explanation": "Creates array of matching elements."}
    ],
    "high": [
        {"question": "What is event delegation?", "options": ["A. Parent handling", "B. Child handling", "C. Direct binding", "D. None"], "answer": "A", "explanation": "Handles events on parent element."},
        {"question": "What is a generator?", "options": ["A. Yields values", "B. Returns once", "C. Loops", "D. None"], "answer": "A", "explanation": "Function that can pause and resume."},
        {"question": "What is 'prototype'?", "options": ["A. Inheritance base", "B. Class definition", "C. Variable", "D. None"], "answer": "A", "explanation": "Basis for object inheritance."},
        {"question": "What is hoisting?", "options": ["A. Declaration lift", "B. Execution delay", "C. Scope change", "D. None"], "answer": "A", "explanation": "Moves declarations to top."},
        {"question": "What is a module?", "options": ["A. Code encapsulation", "B. Global code", "C. Function", "D. None"], "answer": "A", "explanation": "Reusable code unit."},
        {"question": "What is 'fetch' API?", "options": ["A. HTTP requests", "B. Local storage", "C. DOM access", "D. None"], "answer": "A", "explanation": "Makes network requests."},
        {"question": "What is a proxy?", "options": ["A. Object wrapper", "B. Function wrapper", "C. Variable", "D. None"], "answer": "A", "explanation": "Intercepts object operations."},
        {"question": "What is 'Symbol'?", "options": ["A. Unique identifier", "B. String value", "C. Number", "D. None"], "answer": "A", "explanation": "Creates unique property keys."},
        {"question": "What is throttling?", "options": ["A. Rate limiting", "B. Immediate call", "C. Looping", "D. None"], "answer": "A", "explanation": "Limits function call rate."},
        {"question": "What is debouncing?", "options": ["A. Delays execution", "B. Instant execution", "C. Loops", "D. None"], "answer": "A", "explanation": "Delays function until pause."}
    ]
},
            "NodeJS": {
    "easy": [
        {"question": "What is Node.js?", "options": ["A. JS runtime", "B. Browser engine", "C. Database", "D. None"], "answer": "A", "explanation": "Runs JavaScript outside browser."},
        {"question": "What does 'require()' do?", "options": ["A. Imports modules", "B. Exports code", "C. Defines function", "D. None"], "answer": "A", "explanation": "Loads external modules."},
        {"question": "What is 'process' object?", "options": ["A. Runtime info", "B. DOM access", "C. File system", "D. None"], "answer": "A", "explanation": "Provides process information."},
        {"question": "What does 'npm' stand for?", "options": ["A. Node Package Manager", "B. Node Process Manager", "C. Node Programming Module", "D. None"], "answer": "A", "explanation": "Manages Node packages."},
        {"question": "What is 'fs' module?", "options": ["A. File system", "B. Function system", "C. Fetch system", "D. None"], "answer": "A", "explanation": "Handles file operations."},
        {"question": "What does 'http' module do?", "options": ["A. Creates servers", "B. Manages files", "C. Defines variables", "D. None"], "answer": "A", "explanation": "Builds HTTP servers."},
        {"question": "What is an event in Node.js?", "options": ["A. Action trigger", "B. Variable", "C. Class", "D. None"], "answer": "A", "explanation": "Something that can be reacted to."},
        {"question": "What does 'console.log()' do?", "options": ["A. Prints output", "B. Reads input", "C. Creates file", "D. None"], "answer": "A", "explanation": "Logs to terminal."},
        {"question": "What is 'module.exports'?", "options": ["A. Shares code", "B. Imports code", "C. Defines function", "D. None"], "answer": "A", "explanation": "Exports module functionality."},
        {"question": "What is a callback in Node.js?", "options": ["A. Async function", "B. Sync function", "C. Variable", "D. None"], "answer": "A", "explanation": "Function passed as argument."}
    ],
    "intermediate": [
        {"question": "What is the Event Loop?", "options": ["A. Handles async", "B. Loops variables", "C. Defines classes", "D. None"], "answer": "A", "explanation": "Manages asynchronous operations."},
        {"question": "What does 'path' module do?", "options": ["A. File paths", "B. HTTP paths", "C. Function paths", "D. None"], "answer": "A", "explanation": "Handles file system paths."},
        {"question": "What is a Buffer?", "options": ["A. Raw data", "B. String data", "C. Function", "D. None"], "answer": "A", "explanation": "Handles binary data."},
        {"question": "What does 'express' do?", "options": ["A. Web framework", "B. File system", "C. Database", "D. None"], "answer": "A", "explanation": "Simplifies server creation."},
        {"question": "What is 'async/await' in Node.js?", "options": ["A. Simplifies promises", "B. Blocks code", "C. Loops", "D. None"], "answer": "A", "explanation": "Handles async operations cleanly."},
        {"question": "What does 'os' module provide?", "options": ["A. System info", "B. File info", "C. Network info", "D. None"], "answer": "A", "explanation": "Operating system details."},
        {"question": "What is a stream?", "options": ["A. Data flow", "B. Static data", "C. Function", "D. None"], "answer": "A", "explanation": "Handles data in chunks."},
        {"question": "What does 'child_process' do?", "options": ["A. Spawns processes", "B. Kills processes", "C. Defines variables", "D. None"], "answer": "A", "explanation": "Runs external processes."},
        {"question": "What is 'npm install'?", "options": ["A. Adds packages", "B. Removes packages", "C. Updates Node", "D. None"], "answer": "A", "explanation": "Installs dependencies."},
        {"question": "What is 'package.json'?", "options": ["A. Project config", "B. Code file", "C. Style file", "D. None"], "answer": "A", "explanation": "Defines project metadata."}
    ],
    "high": [
        {"question": "What is clustering?", "options": ["A. Multi-core use", "B. Single thread", "C. File grouping", "D. None"], "answer": "A", "explanation": "Utilizes multiple CPU cores."},
        {"question": "What is 'worker_threads'?", "options": ["A. Parallel tasks", "B. Single thread", "C. File tasks", "D. None"], "answer": "A", "explanation": "Runs JS in parallel threads."},
        {"question": "What is a middleware?", "options": ["A. Request handler", "B. Response creator", "C. Variable", "D. None"], "answer": "A", "explanation": "Processes requests in Express."},
        {"question": "What is 'libuv'?", "options": ["A. Event loop engine", "B. JS engine", "C. File system", "D. None"], "answer": "A", "explanation": "Handles async I/O in Node.js."},
        {"question": "What is 'pm2'?", "options": ["A. Process manager", "B. Package manager", "C. Module loader", "D. None"], "answer": "A", "explanation": "Manages Node.js processes."},
        {"question": "What is a REPL?", "options": ["A. Interactive shell", "B. File editor", "C. Compiler", "D. None"], "answer": "A", "explanation": "Read-Eval-Print-Loop for testing."},
        {"question": "What does 'crypto' module do?", "options": ["A. Encryption", "B. File reading", "C. Networking", "D. None"], "answer": "A", "explanation": "Handles cryptographic operations."},
        {"question": "What is 'dotenv'?", "options": ["A. Env variables", "B. File paths", "C. HTTP headers", "D. None"], "answer": "A", "explanation": "Loads environment variables."},
        {"question": "What is a WebSocket?", "options": ["A. Real-time comms", "B. Static comms", "C. File transfer", "D. None"], "answer": "A", "explanation": "Enables bidirectional communication."},
        {"question": "What is 'node:events'?", "options": ["A. Event handling", "B. File handling", "C. Style handling", "D. None"], "answer": "A", "explanation": "Core event emitter module."}
    ]
},
            "Angular": {
    "easy": [
        {"question": "What is Angular?", "options": ["A. JS framework", "B. CSS library", "C. Database", "D. None"], "answer": "A", "explanation": "Framework for building web apps."},
        {"question": "What is a component?", "options": ["A. UI building block", "B. Server function", "C. Variable", "D. None"], "answer": "A", "explanation": "Encapsulates template and logic."},
        {"question": "What does '@Component' do?", "options": ["A. Defines component", "B. Styles component", "C. Deletes component", "D. None"], "answer": "A", "explanation": "Decorator for component metadata."},
        {"question": "What is a template?", "options": ["A. HTML view", "B. CSS style", "C. JS code", "D. None"], "answer": "A", "explanation": "Defines component's UI."},
        {"question": "What is data binding?", "options": ["A. Syncs data", "B. Deletes data", "C. Styles data", "D. None"], "answer": "A", "explanation": "Connects DOM and component."},
        {"question": "What does 'ng serve' do?", "options": ["A. Runs app", "B. Builds app", "C. Tests app", "D. None"], "answer": "A", "explanation": "Starts development server."},
        {"question": "What is a module?", "options": ["A. Code organizer", "B. Single file", "C. Style sheet", "D. None"], "answer": "A", "explanation": "Groups related functionality."},
        {"question": "What does '@NgModule' do?", "options": ["A. Defines module", "B. Defines component", "C. Defines service", "D. None"], "answer": "A", "explanation": "Decorator for module metadata."},
        {"question": "What is 'ngIf'?", "options": ["A. Conditional display", "B. Loop", "C. Event", "D. None"], "answer": "A", "explanation": "Shows/hides elements conditionally."},
        {"question": "What is TypeScript?", "options": ["A. JS superset", "B. CSS variant", "C. HTML extension", "D. None"], "answer": "A", "explanation": "Adds types to JavaScript."}
    ],
    "intermediate": [
        {"question": "What is a service?", "options": ["A. Shared logic", "B. UI component", "C. Style sheet", "D. None"], "answer": "A", "explanation": "Handles business logic."},
        {"question": "What does '@Injectable()' do?", "options": ["A. Marks service", "B. Marks component", "C. Marks module", "D. None"], "answer": "A", "explanation": "Makes class injectable."},
        {"question": "What is dependency injection?", "options": ["A. Provides services", "B. Deletes services", "C. Styles services", "D. None"], "answer": "A", "explanation": "Injects dependencies into classes."},
        {"question": "What is 'ngFor'?", "options": ["A. Loops over list", "B. Conditions", "C. Events", "D. None"], "answer": "A", "explanation": "Iterates over arrays."},
        {"question": "What is a pipe?", "options": ["A. Transforms data", "B. Fetches data", "C. Styles data", "D. None"], "answer": "A", "explanation": "Formats data in templates."},
        {"question": "What does 'HttpClient' do?", "options": ["A. Makes HTTP requests", "B. Manages files", "C. Defines styles", "D. None"], "answer": "A", "explanation": "Handles API calls."},
        {"question": "What is routing?", "options": ["A. Navigation", "B. Data binding", "C. Styling", "D. None"], "answer": "A", "explanation": "Manages app navigation."},
        {"question": "What does '[(ngModel)]' do?", "options": ["A. Two-way binding", "B. One-way binding", "C. Event binding", "D. None"], "answer": "A", "explanation": "Syncs input with data."},
        {"question": "What is an observable?", "options": ["A. Async data", "B. Sync data", "C. Static data", "D. None"], "answer": "A", "explanation": "Stream of data over time."},
        {"question": "What does 'ngOnInit()' do?", "options": ["A. Initializes component", "B. Destroys component", "C. Styles component", "D. None"], "answer": "A", "explanation": "Lifecycle hook for initialization."}
    ],
    "high": [
        {"question": "What is lazy loading?", "options": ["A. Delayed modules", "B. Immediate load", "C. Style load", "D. None"], "answer": "A", "explanation": "Loads modules on demand."},
        {"question": "What is a resolver?", "options": ["A. Pre-fetches data", "B. Deletes data", "C. Styles data", "D. None"], "answer": "A", "explanation": "Fetches data before route loads."},
        {"question": "What is RxJS?", "options": ["A. Reactive library", "B. Routing library", "C. Styling library", "D. None"], "answer": "A", "explanation": "Handles reactive programming."},
        {"question": "What is a guard?", "options": ["A. Route protection", "B. Data fetch", "C. Style apply", "D. None"], "answer": "A", "explanation": "Controls route access."},
        {"question": "What is change detection?", "options": ["A. Updates UI", "B. Deletes UI", "C. Styles UI", "D. None"], "answer": "A", "explanation": "Syncs data with view."},
        {"question": "What is a directive?", "options": ["A. Custom behavior", "B. Standard tag", "C. Module", "D. None"], "answer": "A", "explanation": "Extends HTML functionality."},
        {"question": "What does 'ngZone' do?", "options": ["A. Optimizes updates", "B. Fetches data", "C. Defines styles", "D. None"], "answer": "A", "explanation": "Manages change detection zones."},
        {"question": "What is AOT compilation?", "options": ["A. Ahead-of-time", "B. Just-in-time", "C. Runtime", "D. None"], "answer": "A", "explanation": "Compiles during build for performance."},
        {"question": "What is a structural directive?", "options": ["A. Alters DOM", "B. Styles DOM", "C. Fetches DOM", "D. None"], "answer": "A", "explanation": "Changes DOM structure."},
        {"question": "What is Angular Universal?", "options": ["A. Server rendering", "B. Client rendering", "C. Style rendering", "D. None"], "answer": "A", "explanation": "Renders app on server."}
    ]
        }
}

class QuizVolution:
    def __init__(self):
        self.quiz_data = []
        self.user_profile = {
            "name": "", "email": "", "education_level": "", "languages": [],
            "difficulty": "easy", "response_times": [], "score": 0, "send_email": False,
            "history": []
        }
        self.current_question = 0

    def fetch_questions(self, languages, difficulty):
        self.quiz_data = []
        for lang in languages:
            if lang in sample_questions and difficulty in sample_questions[lang]:
                available_questions = sample_questions[lang][difficulty]
                self.quiz_data.extend(available_questions[:min(10 - len(self.quiz_data), len(available_questions))])
                if len(self.quiz_data) >= 10:
                    break
        random.shuffle(self.quiz_data)
        return bool(self.quiz_data)

    def generate_report(self):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(f"QuizVolution Report for {self.user_profile['name']}", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Score: {self.user_profile['score']} / {len(self.quiz_data)}", styles['Heading2']))
        avg_time = sum(self.user_profile["response_times"]) / len(self.user_profile["response_times"]) if self.user_profile["response_times"] else 0
        story.append(Paragraph(f"Average Response Time: {avg_time:.2f} seconds", styles['Normal']))
        story.append(Paragraph(f"Languages: {', '.join(self.user_profile['languages'])}", styles['Normal']))
        story.append(Paragraph(f"Education: {self.user_profile['education_level']}", styles['Normal']))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Performance Breakdown", styles['Heading2']))
        data = [["Question No.", "Question", "Your Answer", "Correct Answer", "Result", "Time (s)"]]
        for i, entry in enumerate(self.user_profile["history"], 1):
            data.append([
                str(i),
                entry["question"][:30] + "..." if len(entry["question"]) > 30 else entry["question"],
                entry["user_answer"],
                entry["correct_answer"],
                "Correct" if entry["correct"] else "Wrong",
                f"{entry['time']:.2f}"
            ])
        table = Table(data, colWidths=[50, 100, 80, 80, 60, 60])
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#1e90ff'),
            ('TEXTCOLOR', (0, 0), (-1, 0), '#ffffff'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, '#000000'),
        ])
        story.append(table)

        doc.build(story)
        buffer.seek(0)
        return buffer

def get_user_quiz():
    if 'quiz_state' not in session:
        session['quiz_state'] = QuizVolution().__dict__
    quiz = QuizVolution()
    quiz.__dict__.update(session['quiz_state'])
    return quiz

def save_user_quiz(quiz):
    session['quiz_state'] = quiz.__dict__
    session.modified = True  # Ensure session updates

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        quiz = QuizVolution()
        quiz.user_profile["name"] = request.form.get('name')
        quiz.user_profile["email"] = request.form.get('email')
        quiz.user_profile["education_level"] = request.form.get('education')
        quiz.user_profile["languages"] = request.form.getlist('languages') or ["all"]
        quiz.user_profile["difficulty"] = request.form.get('difficulty')
        quiz.user_profile["send_email"] = request.form.get('send_email') == 'on'

        if "all" in quiz.user_profile["languages"]:
            quiz.user_profile["languages"] = list(sample_questions.keys())

        if not quiz.fetch_questions(quiz.user_profile["languages"], quiz.user_profile["difficulty"]):
            return render_template('start.html', error="No questions available for the selected options.")

        quiz.current_question = 0
        quiz.user_profile["score"] = 0
        quiz.user_profile["response_times"] = []
        quiz.user_profile["history"] = []
        save_user_quiz(quiz)
        print(f"Quiz initialized: {len(quiz.quiz_data)} questions")  # Debugging
        return render_template('quiz.html', question=quiz.quiz_data[0], q_num=1, total=len(quiz.quiz_data))
    return render_template('start.html')

@app.route('/quiz', methods=['POST'])
def quiz_page():
    quiz = get_user_quiz()
    answer = request.form.get('answer')
    start_time = float(request.form.get('start_time'))
    response_time = time.time() - start_time

    print(f"Processing question {quiz.current_question + 1}/{len(quiz.quiz_data)}")  # Debugging

    # Process the current question
    current = quiz.quiz_data[quiz.current_question]
    quiz.user_profile["response_times"].append(response_time)
    correct = answer == current['answer']
    if correct:
        quiz.user_profile["score"] += 1
        result = "Correct!"
    else:
        result = f"Wrong. Correct answer: {current['answer']}"

    # Record history
    quiz.user_profile["history"].append({
        "question": current["question"],
        "user_answer": answer,
        "correct_answer": current["answer"],
        "correct": correct,
        "time": response_time
    })

    # Move to next question and save state
    quiz.current_question += 1
    save_user_quiz(quiz)

    # Check if quiz is complete
    if quiz.current_question >= len(quiz.quiz_data):
        print("Quiz complete, redirecting to results")  # Debugging
        if quiz.user_profile["send_email"]:
            send_email(quiz.user_profile["email"], quiz.user_profile["score"], len(quiz.quiz_data), quiz.user_profile["languages"])
        avg_response_time = sum(quiz.user_profile["response_times"]) / len(quiz.user_profile["response_times"]) if quiz.user_profile["response_times"] else 0
        return render_template('results.html', score=quiz.user_profile["score"], total=len(quiz.quiz_data),
                              profile=quiz.user_profile, avg_response_time=avg_response_time)

    # Render next question
    print(f"Rendering next question {quiz.current_question + 1}")  # Debugging
    return render_template('quiz.html', question=quiz.quiz_data[quiz.current_question],
                          q_num=quiz.current_question + 1, total=len(quiz.quiz_data),
                          result=result, explanation=current['explanation'])

@app.route('/download_report')
def download_report():
    quiz = get_user_quiz()
    print(f"Generating report for {quiz.user_profile['name']}, score: {quiz.user_profile['score']}")  # Debugging
    buffer = quiz.generate_report()
    return Response(buffer.getvalue(), mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=quizvolution_report_{quiz.user_profile["name"]}.pdf'})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)