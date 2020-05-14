
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-nli-mean-tokens')


'''
sentences = ['Demonstrating the ability to work effectively with others.',
'Interact professionally and respectfully with supervisors and coworkers.',
'Work effectively with people who have diverse personalities and backgrounds.',
'Respect the opinions, perspectives, customs, contributions, and individual differences of others.',
'Use appropriate strategies and solutions for dealing with conflicts and differences to maintain a smooth workflow.',
'Be flexible and open-minded when dealing with a wide range of people.',
'Listen to and consider others’ viewpoints.',
'Integrity:  Displaying accepted social and work behaviors.',
'Treat others with honesty, fairness, and respect.',
'Comply with ethical standards for your field.',
'Take responsibility for accomplishing work goals within accepted timeframes.',
'Accept responsibility for one’s decisions and actions.',
'Perform quality work.',
'Professionalism:  Maintaining a socially acceptable demeanor.',
'Demonstrate self-control by maintaining composure and dealing calmly with stressful situations.',
'Accept criticism and attempt to learn from mistakes.',
'Demonstrate a positive attitude towards work.',
'Follow rules and standards of dress.',
'Follow rules and standards of personal hygiene.',
'Refrain from substance abuse.',
'Initiative:  Demonstrating a willingness to work.',
'Take initiative in seeking out new responsibilities and work challenges.',
'Pursue work with energy, drive, and effort to accomplish tasks.',
'Persist at a task until completion, despite interruptions, obstacles, or setbacks.',
'Establish and maintain personally challenging, but realistic work goals.',
'Strive to exceed standards and expectations.',
'Dependability & Reliability:  Displaying responsible behaviors at work.', 
'Behave consistently, predictably, and reliably.',
'Fulfill obligations, complete assignments, and meet deadlines.',
'Follow written and verbal directions.',
'Comply with organizational rules, policies, and procedures.',
'Lifelong Learning:  Displaying a willingness to learn and apply new knowledge and skills.',
'Demonstrate an interest in personal and professional lifelong learning and development.',
'Treat unexpected circumstances as opportunities to learn and adopt new techniques.',
'Seek feedback, and modify behavior for improvement.',
'Broaden knowledge and skills through job shadowing and continuing education.',
'Use newly learned knowledge and skills to complete specific tasks and improve work processes.',
'Take charge of personal career development by identifying personal interests and career pathways',
'Seek and maintain membership in professional associations', 
"Read technical publications to stay abreast of new developments in the industry",  
"Maintain certifications and continuing education credits"]
    '''
bok_sent_emb = ['the ability to work effectively with others', 'self-control', 'a positive attitude towards work', 'a willingness to work', 'an interest in personal and professional lifelong learning and development', 'the opinions, perspectives, customs, contributions, and individual differences of others', 'appropriate strategies and solutions for dealing with conflicts and differences to maintain a smooth workflow', 'a smooth workflow', 'a socially acceptable demeanor', 'composure', 'membership in professional associations', 'certifications and continuing education credits', 'othersâ€™ viewpoints', 'accepted social and work behaviors', 'responsible behaviors', 'a willingness to learn and apply new knowledge and skills', 'others', 'unexpected circumstances', 'responsibility for accomplishing work goals within accepted timeframes', 'initiative', 'charge of personal career development', 'work goals within accepted timeframes', 'tasks', 'responsibility for oneâ€™s decisions and actions', 'criticism', 'quality work', 'rules and standards of dress', 'rules and standards of personal hygiene', 'written and verbal directions', 'new responsibilities and work challenges', 'feedback', 'work with energy, drive, and effort to accomplish tasks', 'standards and expectations', 'obligations, complete assignments, and', 'deadlines', 'new knowledge and skills', 'new techniques', 'behavior', 'knowledge and skills', 'specific tasks', 'work processes', 'personal interests and career pathways', 'technical publications']

sentence_embeddings = model.encode(bok_sent_emb)

print('Sample BERT embedding vector - length', len(sentence_embeddings[0]))

print('Sample BERT embedding vector - note includes negative values', sentence_embeddings[0])



col_query_sent = ['the foundation for electronic circuits and measurements', 'basic instruction', 'an overview of the manufacturing processes utilized in advanced manufacturing facilities as well as the materials most likely to be encountered', 'the student', 'the foundation for both mechanical and electronic measurement techniques encountered in the advanced manufacturing environment', 'a theory of operation of direct current (dc', 'principles of electricity, magnetism, and basic laws of electronics', 'fundamentals of dc circuits, ac circuits, semiconductors, and digital circuits', 'the define, measure, analyze, improve, and control', 'digital sensors, optical and magnetic switches, pressure, temperature, and piezoelectric sensors', 'demonstration and setting up various hydraulic and pneumatic circuits', 'pid', 'review of algebraic techniques or operations, radicals, exponents, complex numbers, absolute value, linear and quadratic equations and inequalities, exponential and logarithmic functions, simultaneous equations and inequalities, roots of polynomials, matrices, determinants, applications, mathematical proof techniques, mathematical induction, binomial theorem, sequences and series', 'the conceptual measurements', 'the conceptual measurements', 'electricity and electronics', 'ac and dc electric circuit theory', 'the various functions of manufacturing and their complex interrelationships', 'the meaning and application of osha standards', 'material safety data sheets (msds) information', 'fire safety and emergency response', 'workplace ergonomics', 'the basic concepts of lean, based on the toyota production system', 'the rollout process', 'the six sigma process and its impact on quality, customer satisfaction and costs', 'the concepts of measurement and metrology', 'the basic features of measurement, gauging and tolerances', 'the different types of electronic measurement', 'the basic measurement techniques for electronic circuits', 'industrial applications of fluid power', 'the functions of basic hydraulic system components', 'the unique nature of pneumatic systems', 'electrical controls and electro-hydraulic systems', 'electrical drawings and motor safety', 'circuits', 'electronic circuits.this course', 'advanced hydraulic circuits', 'a process to identify and correct problems', 'circuit models to solve electrical problems', 'tools and equipment', 'safety lockout and tag-out procedures', 'basic electronic testing equipment', 'control systems', 'electrical problems', 'real-world problems', 'application problems that involve trigonometric functions', 'trigonometric equations and inverse trigonometric equations', 'right and oblique triangles', 'systems of linear and nonlinear equations', 'all types of equations— linear, quadratic, higher order polynomial, exponential and logarithmic—', 'second degree and higher inequalities', 'application problems from various disciplines', 'circuit techniques', 'principles of robotics', 'mathematical concepts', 'instruments and electronic workstations', 'computer simulation techniques', 'autocad', 'basic draw', 'charts or records', 'hand and power tools', 'tools, instruments, and testing devices', 'it', 'real and imaginary numbers', 'appropriate term and summation formulas and notation', 'drafting (cad) systems using autocad', 'a series of review exercises and drawings', 'a working knowledge within the autocad environment to set-up drawing files', 'knowledge using basic draw and modify commands to create autocad drawings', 'an understanding of a quality process’s capabilities and its applications', 'knowledge of how to implement quality assurance principles/methods and checks for inspections', 'an understanding of internal and external supply chains, inventory control methods, and configuration of management', 'knowledge of production floor plan and safety requirements to place materials in most efficient and safe location', 'knowledge of forecasting methods, audits, cycle count process, and trade-off techniques', 'knowledge of the criteria for tool design, maintenance, procurement, and handling', 'an understanding of the importance and impact of routine maintenance of machines and equipment on operations', 'knowledge of the language and systems of measurement', 'an understanding of dc and ac motors, three-phase and single-phase, and motor drives', 'an ability to select, install, maintain, and troubleshoot motors', 'knowledge of motor control circuits and electronics, as well as adjustable speed', 'knowledge of industrial processes and control systems', 'proficiency in using tools, instruments, and testing devices', 'basic troubleshooting skills', 'drawing files', 'various hydraulic and pneumatic circuits', 'commands', 'autocad drawings', 'annotations', 'a human machine interface', 'the proper use of display and inquiry commands', 'an overall knowledge of the production process', 'drawing files', 'their basic personal computing skills', 'use of technology', 'basic drafting concepts.this course', 'the student', 'quality', 'the quality standards required in the advanced manufacturing environment', 'processes for quality', 'process measurements', 'root causes, preventive action, and corrective action', 'advantages and disadvantages of hydraulic and pneumatic systems', 'control systems components and software', 'manufacturing networks where control systems may be utilized', 'the characteristics of a given family of functions.this course', 'deals with the solution of triangles, trigonometric relations, and functions of an angle, logarithms, and complex numbers', 'arithmetic and geometric terms and sequences using appropriate term and summation formulas and notation', 'quality assurance principles/methods and checks for inspections', 'materials', 'manufacturing instruments', 'the knowledge and skills needed to create and maintain a safe and productive work environment as defined by osha regulations that are applicable to advanced manufacturing facilities', 'industrial electrical wiring and instrumentation, including digital sensors, optical and magnetic switches, pressure, temperature, and piezoelectric sensors', 'fundamental ladder logic, programmable controller theory and application techniques, and design and troubleshooting of plc-based (programmable logic controller) systems in classroom presentations, lab construction and redesign, simulation trainers, and multi-modal software learning labs', 'a safe and productive work environment', 'safety inspections', 'others', 'blood-borne pathogens', 'trigonometric functions', 'the tools supporting the lean model', 'the lean model', 'areas of improvement and the correct lean tools to utilize', 'motor control devices such as switches, sensors, actuators, contactors, motor starters, relays, and transformers\n', 'peer- to-peer appraisals based on lean transformation leadership requirements', 'principles of fluid and airflow', 'maintenance and troubleshooting techniques', 'basic pneumatic control and logic circuit design and operation', 'calculations using real and imaginary numbers', 'operations on rectangular and polar form of complex numbers.topics', 'operations', 'current (ac) motors', 'motors', 'a process', 'systems.this course', 'a project', 'local modules', 'basic ladder logic', 'ladder logic', 'the various formats of a function – symbolic, numerical, visual and verbal', 'the domain and range of trigonometric functions and inverse trigonometric functions', 'the domain and range of a function presented in various formats and intervals over which a function is increasing or decreasing', 'angle measurements between degree and radian units', 'trigonometric identities', 'all types of equations—', 'linear, quadratic, higher order polynomial, exponential, logarithmic, and conic sections']



import scipy
from sklearn.metrics.pairwise import cosine_similarity


#query = 'Attention is given to study habits, vocational choice and the development of a well-rounded philosophy of life.' #@param {type: 'string'}
tier1_nouns = []
for query in col_query_sent:
    queries = [query]
    query_embeddings = model.encode(queries)

    # Find the closest 3 sentences of the corpus for each query sentence based on cosine similarity
    number_top_matches = 3 #@param {type: "number"}

    print("Semantic Search Results")

    for query, query_embedding in zip(queries, query_embeddings):
        #distances = scipy.spatial.distance.cdist([query_embedding], sentence_embeddings, "cosine")[0]
        distances = cosine_similarity([query_embedding], sentence_embeddings)[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 5 most similar sentences in corpus:")

        for indx, (idx, distance) in enumerate(results[0:number_top_matches]):
            print(bok_sent_emb[idx].strip(), "(Cosine Score: %.4f)" % (1-distance))
            print("indx: ", indx, " similarity: ", (1-distance))
            if indx == 0 and ((1-distance) > 0.85): 
                tier1_nouns.append(query)
print("Categorized nouns",tier1_nouns)


