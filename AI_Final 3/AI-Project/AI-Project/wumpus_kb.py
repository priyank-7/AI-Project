import utils

#-------------------------------------------------------------------------------
# Wumpus Propositions
#-------------------------------------------------------------------------------

### atemporal variables

proposition_bases_atemporal_location = ['P', 'W', 'S', 'B']

def pit_str(x, y):
    "There is a Pit at <x>,<y>"
    return 'P{0}_{1}'.format(x, y)
def wumpus_str(x, y):
    "There is a Wumpus at <x>,<y>"
    return 'W{0}_{1}'.format(x, y)
def stench_str(x, y):
    "There is a Stench at <x>,<y>"
    return 'S{0}_{1}'.format(x, y)
def breeze_str(x, y):
    "There is a Breeze at <x>,<y>"
    return 'B{0}_{1}'.format(x, y)

### fluents (every proposition who's truth depends on time)

proposition_bases_perceptual_fluents = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']

def percept_stench_str(t):
    "A Stench is perceived at time <t>"
    return 'Stench{0}'.format(t)
def percept_breeze_str(t):
    "A Breeze is perceived at time <t>"
    return 'Breeze{0}'.format(t)
def percept_glitter_str(t):
    "A Glitter is perceived at time <t>"
    return 'Glitter{0}'.format(t)
def percept_bump_str(t):
    "A Bump is perceived at time <t>"
    return 'Bump{0}'.format(t)
def percept_scream_str(t):
    "A Scream is perceived at time <t>"
    return 'Scream{0}'.format(t)

proposition_bases_location_fluents = ['OK', 'L']

def state_OK_str(x, y, t):
    "Location <x>,<y> is OK at time <t>"
    return 'OK{0}{1}{2}'.format(x, y, t)
def state_loc_str(x, y, t):
    "At Location <x>,<y> at time <t>"
    return 'L{0}{1}{2}'.format(x, y, t)

def loc_proposition_to_tuple(loc_prop):
    """
    Utility to convert location propositions to location (x,y) tuples
    Used by HybridWumpusAgent for internal bookkeeping.
    """
    parts = loc_prop.split('_')
    return (int(parts[0][1:]), int(parts[1]))

proposition_bases_state_fluents = ['HeadingNorth', 'HeadingEast',
                                   'HeadingSouth', 'HeadingWest',
                                   'HaveArrow', 'WumpusAlive']

def state_heading_north_str(t):
    "Heading North at time <t>"
    return 'HeadingNorth{0}'.format(t)
def state_heading_east_str(t):
    "Heading East at time <t>"
    return 'HeadingEast{0}'.format(t)
def state_heading_south_str(t):
    "Heading South at time <t>"
    return 'HeadingSouth{0}'.format(t)
def state_heading_west_str(t):
    "Heading West at time <t>"
    return 'HeadingWest{0}'.format(t)
def state_have_arrow_str(t):
    "Have Arrow at time <t>"
    return 'HaveArrow{0}'.format(t)
def state_wumpus_alive_str(t):
    "Wumpus is Alive at time <t>"
    return 'WumpusAlive{0}'.format(t)

proposition_bases_actions = ['Forward', 'Grab', 'Shoot', 'Climb',
                             'TurnLeft', 'TurnRight', 'Wait']

def action_forward_str(t=None):
    "Action Forward executed at time <t>"
    return ('Forward{0}'.format(t) if t != None else 'Forward')
def action_grab_str(t=None):
    "Action Grab executed at time <t>"
    return ('Grab{0}'.format(t) if t != None else 'Grab')
def action_shoot_str(t=None):
    "Action Shoot executed at time <t>"
    return ('Shoot{0}'.format(t) if t != None else 'Shoot')
def action_climb_str(t=None):
    "Action Climb executed at time <t>"
    return ('Climb{0}'.format(t) if t != None else 'Climb')
def action_turn_left_str(t=None):
    "Action Turn Left executed at time <t>"
    return ('TurnLeft{0}'.format(t) if t != None else 'TurnLeft')
def action_turn_right_str(t=None):
    "Action Turn Right executed at time <t>"
    return ('TurnRight{0}'.format(t) if t != None else 'TurnRight')
def action_wait_str(t=None):
    "Action Wait executed at time <t>"
    return ('Wait{0}'.format(t) if t != None else 'Wait')


def add_time_stamp(prop, t): return '{0}{1}'.format(prop, t)

proposition_bases_all = [proposition_bases_atemporal_location,
                         proposition_bases_perceptual_fluents,
                         proposition_bases_location_fluents,
                         proposition_bases_state_fluents,
                         proposition_bases_actions]


#-------------------------------------------------------------------------------
# Axiom Generator: Current Percept Sentence
#-------------------------------------------------------------------------------

"""
Name: Priyal Patel
"""
def axiom_generator_percept_sentence(t, tvec):
    """
    Asserts that each percept proposition is True or False at time t.

    t := time
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)

    Example:
        Input:  [False, True, False, False, True]
        Output: '~Stench0 & Breeze0 & ~Glitter0 & ~Bump0 & Scream0'
    """

    percept_seq = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']
    for i in range(len(tvec)):
        if not tvec[i]:
            percept_seq[i] = "~" + percept_seq[i]
        percept_seq[i]+=str(t)
    return (" & ".join(percept_seq))
"""
Name: Priyal Patel
"""
def axiom_generator_initial_location_assertions(x, y):
    """
    Assert that there is no Pit and no Wumpus in the location

    x,y := the location
    """
    return ("" + pit_str(x,y) + " & " + "" + wumpus_str(x,y))


"""
Name: Priyal Patel
"""
def axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Breezes (atemporal) are only found in locations where
    there are one or more Pits in a neighboring location (or the same location!)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Pits).
    """
    axiom_str = ''

    pits = []
    for (xVal,yVal) in [((x-1),y),(x,(y-1)),((x+1),y),(x,(y+1))]:
        if xVal >= xmin and xVal <= xmax and yVal >= ymin and yVal <= ymax:
            pits.append(pit_str(xVal,yVal)) 
    pits.append('P'+str(x)+'_'+str(y))
    axiom_str += '{0} <=> ({1})'.format(breeze_str(x,y),(' | ').join(pits))

    return axiom_str

    

def generate_pit_and_breeze_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_pits_and_breezes')

    return axioms


"""
Name: Priyal Patel
"""
def axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Stenches (atemporal) are only found in locations where
    there are one or more Wumpi in a neighboring location (or the same location!)

    (Don't try to assert here that there is only one Wumpus;
    we'll handle that separately)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Wumpi).
    """
    wumpus = []
    for i, j in [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]:
        if xmin <= i <= xmax and ymin <= j <= ymax:
            wumpus.append(wumpus_str(i, j))
    wumpus.append(wumpus_str(x, y))

    return (stench_str(x,y) + " <=> (" + (" | ").join(wumpus) + ")")


def generate_wumpus_and_stench_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):

        utils.print_not_implemented('axiom_generator_wumpus_and_stench')
    return axioms


"""
Name: Priyam Shah
"""
def axiom_generator_at_least_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at least one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    for i in range(xmin,xmax + 1):
        for j in range(ymin, ymax + 1):
            if (i!=xmax) or (j!=ymax):
                axiom_str+=(wumpus_str(i, j))+" | "
            else:
                axiom_str+=wumpus_str(i,j)

    return axiom_str


"""
Name: Priyam Shah
"""
def axiom_generator_at_most_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at at most one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    # rooms = ['~' + wumpus_str(xVal,yVal) for xVal in range(xmin,xmax + 1) for yVal in range(ymin,ymax + 1)]
    # axiom_str = ' | '.join(rooms)
    # return axiom_str

    axioms = []
    grid = [(i,j) for i in range(xmin, xmax + 1) for j in range(ymin, ymax + 1)]

    for x in grid:
        nowumpus =[]
        for y in grid:
            if x != y:
                    nowumpus.append("~" + wumpus_str(y[0], y[1]))
    axioms.append("(" + wumpus_str(x[0],x[1]) + " >> ("+ (" & ".join(nowumpus)) +"))")
    
    axiom_str = ' & '.join(axioms)
    return axiom_str


"""
Name: Priyam Shah
"""
def axiom_generator_only_in_one_location(xi, yi, xmin, xmax, ymin, ymax, t=0):
    """
    Assert that the Agent can only be in one (the current xi,yi) location at time t.

    xi,yi := the current location.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    t := time; default=0
    """
    possible_locations = []
    l=[]
    for i in range(xmin, xmax + 1):
        for j in range(ymin, ymax + 1):
            possible_locations.append(state_loc_str(i, j,t))
    
    for i in possible_locations:
        if i!=state_loc_str(xi,yi,t):
            l.append(i)
    possible_locations = l
    return state_loc_str(xi,yi,t) + " & ~(" + (" | ").join(possible_locations) + ")"


"""
Name: Priyam Shah
"""
def axiom_generator_only_one_heading(heading='north', t=0):
    """
    Assert that Agent can only head in one direction at a time.

    heading := string indicating heading; default='north';
               will be one of: 'north', 'east', 'south', 'west'
    t := time; default=0
    """
    axiom_str = ''
    entetes = [
    	"~" + state_heading_north_str(t),
    	"~" + state_heading_east_str(t),
    	"~" + state_heading_south_str(t),
    	"~" + state_heading_west_str(t)
    ]
    index = {"north":0, "east":1, "south":2, "west":3}

    indexmodif = index[heading]
    entetes[indexmodif] = entetes[indexmodif][1:]

    axiom_str = " & ".join(entetes)
    return axiom_str

"""
Name: Mujtaba jafri
"""
def axiom_generator_have_arrow_and_wumpus_alive(t=0):
    """
    Assert that Agent has the arrow and the Wumpus is alive at time t.

    t := time; default=0
    """
    have_arrow = state_have_arrow_str(t)
    wumpus_alive = state_wumpus_alive_str(t)
    axiom = have_arrow + " & " + wumpus_alive
    return axiom


def initial_wumpus_axioms(xi, yi, width, height, heading='east'):
    """
    Generate all of the initial wumpus axioms
    
    xi,yi = initial location
    width,height = dimensions of world
    heading = str representation of the initial agent heading
    """
    axioms = [axiom_generator_initial_location_assertions(xi, yi)]
    axioms.extend(generate_pit_and_breeze_axioms(1, width, 1, height))
    axioms.extend(generate_wumpus_and_stench_axioms(1, width, 1, height))
    
    axioms.append(axiom_generator_at_least_one_wumpus(1, width, 1, height))
    axioms.append(axiom_generator_at_most_one_wumpus(1, width, 1, height))

    axioms.append(axiom_generator_only_in_one_location(xi, yi, 1, width, 1, height))
    axioms.append(axiom_generator_only_one_heading(heading))

    axioms.append(axiom_generator_have_arrow_and_wumpus_alive())
    
    return axioms


#-------------------------------------------------------------------------------
# Axiom Generators: Temporal Axioms (added at each time step)
#-------------------------------------------------------------------------------


"""
Name: Mujtaba jafri
"""
def axiom_generator_location_OK(x, y, t):
    """
    Assert the conditions under which a location is safe for the Agent.
    (Hint: Are Wumpi always dangerous?)

    x,y := location
    t := time
    """
    return '{0} <=> (~{1} & ({3} >> ~{2}))'.format(state_OK_str(x,y,t),pit_str(x,y),state_wumpus_alive_str(t),wumpus_str(x,y))


def generate_square_OK_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_location_OK(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_location_OK')

    return list(filter(lambda s: s != '', axioms))


#-------------------------------------------------------------------------------
# Connection between breeze / stench percepts and atemporal location properties

"""
Name: Mujtaba jafri
"""
def axiom_generator_breeze_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a breeze
    at that time (a percept) means that the location is breezy (atemporal)

    x,y := location
    t := time
    """
    return f'{state_loc_str(x,y,t)} >> ({percept_breeze_str(t)} % {breeze_str(x,y)})'


def generate_breeze_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_breeze_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_breeze_percept_and_location_property')
    return filter(lambda s: s != '', axioms)


"""
Name: Deeprajsinh Gohil
"""
def axiom_generator_stench_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a stench
    at that time (a percept) means that the location has a stench (atemporal)

    x,y := location
    t := time
    """
    return f'{state_loc_str(x,y,t)} >> ({percept_stench_str(t)} % {stench_str(x,y)})'


def generate_stench_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_stench_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_stench_percept_and_location_property')
    return filter(lambda s: s != '', axioms)


#-------------------------------------------------------------------------------
# Transition model: Successor-State Axioms (SSA's)
# Avoid the frame problem(s): don't write axioms about actions, write axioms about
# fluents!  That is, write successor-state axioms as opposed to effect and frame
# axioms
#
# The general successor-state axioms pattern (where F is a fluent):
#   F^{t+1} <=> (Action(s)ThatCause_F^t) | (F^t & ~Action(s)ThatCauseNot_F^t)

# NOTE: this is very expensive in terms of generating many (~170 per axiom) CNF clauses!


"""
Name: Deeprajsinh Gohil
"""
def axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax):
    """
    Assert the condidtions at time t under which the agent is in
    a particular location (state_loc_str: L) at time t+1, following
    the successor-state axiom pattern.

    See Section 7. of AIMA.  However...
    NOTE: the book's version of this class of axioms is not complete
          for the version in Project 3.

    x,y := location
    t := time
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    
    curr = [f"({state_loc_str(x, y, t)} & (~{action_forward_str(t)} | {percept_bump_str(t+1)} | {action_grab_str(t)} | {action_shoot_str(t)} | {action_turn_left_str(t)} | {action_turn_right_str(t)}))"]
    for ((i, j), temp) in [(((x - 1), y),"E"), ((x, (y - 1)),"N"), (((x + 1), y),"W"), ((x, (y + 1)),"S")]:
        if xmin <= i <= xmax and ymin <= j <= ymax:
            if temp == "N":
                curr.append(f"({state_loc_str(x, y - 1, t)} & ({state_heading_north_str(t)} & {action_forward_str(t)}))")
            if temp == "E":
                curr.append(f"({state_loc_str(x - 1, y, t)} & ({state_heading_east_str(t)} & {action_forward_str(t)}))")
            if temp == "W":
                curr.append(f"({state_loc_str(x + 1, y, t)} & ({state_heading_west_str(t)} & {action_forward_str(t)}))")
            if temp == "S":
                curr.append(f"({state_loc_str(x, y + 1, t)} & ({state_heading_south_str(t)} & {action_forward_str(t)}))")

    return "{0} <=> ({1})".format(state_loc_str(x,y,t+1)," | ".join(curr))

def generate_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax, heading):
    """
    The full at_location SSA converts to a fairly large CNF, which in
    turn causes the KB to grow very fast, slowing overall inference.
    We therefore need to restric generating these axioms as much as possible.
    This fn generates the at_location SSA only for the current location and
    the location the agent is currently facing (in case the agent moves
    forward on the next turn).
    This is sufficient for tracking the current location, which will be the
    single L location that evaluates to True; however, the other locations
    may be False or Unknown.
    """
    axioms = [axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax)]
    if heading == 'west' and x - 1 >= xmin:
        axioms.append(axiom_generator_at_location_ssa(t, x-1, y, xmin, xmax, ymin, ymax))
    if heading == 'east' and x + 1 <= xmax:
        axioms.append(axiom_generator_at_location_ssa(t, x+1, y, xmin, xmax, ymin, ymax))
    if heading == 'south' and y - 1 >= ymin:
        axioms.append(axiom_generator_at_location_ssa(t, x, y-1, xmin, xmax, ymin, ymax))
    if heading == 'north' and y + 1 <= ymax:
        axioms.append(axiom_generator_at_location_ssa(t, x, y+1, xmin, xmax, ymin, ymax))
    return filter(lambda s: s != '', axioms)

#----------------------------------

"""
Name: Priyank Patel
"""
def axiom_generator_have_arrow_ssa(t):
    """
    Assert the conditions at time t under which the Agent
    has the arrow at time t+1

    t := time
    """

    # if the agent didnt shoot arrow at time t and the agent have arrow at previous state then and only then the agent have arrow at time t+1
    arrow_plus_one = state_have_arrow_str(t+1)
    arrow = state_have_arrow_str(t)
    shoot = action_shoot_str(t)
    return arrow_plus_one + " >> (" + arrow + "& ~" + shoot + ")"


"""
Name: Priyank Patel
"""
def axiom_generator_wumpus_alive_ssa(t):
    """
    Assert the conditions at time t under which the Wumpus
    is known to be alive at time t+1

    (NOTE: If this axiom is implemented in the standard way, it is expected
    that it will take one time step after the Wumpus dies before the Agent
    can infer that the Wumpus is actually dead.)

    t := time
    """
    # If wumpus is alive at time t+1 if and only if wumpus alive at time t and the agent didnt hear scream at time t+1
    alive_plus_one = state_wumpus_alive_str(t+1)
    alive = state_wumpus_alive_str(t)
    scream = percept_scream_str(t)
    return alive_plus_one + " <=> (" + alive + "& ~" + scream + ")"

#----------------------------------


"""
Name: Priyank Patel
"""
def axiom_generator_heading_north_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be North at time t+1

    t := time
    """
    heading_north_ssa = state_heading_north_str(t+1)
    action = "({0} & ({1} | {2} | {3} | {4} | {5}))".format(
        state_heading_north_str(t), # the agent is already in the north direction at time t
        action_wait_str(t),         # action wait will not change the direction of the agent if it was in the north direction
        action_grab_str(t),         # action wait will not change the direction of the agent if it was in the north direction
        action_shoot_str(t),        # action wait will not change the direction of the agent if it was in the north direction
        percept_bump_str(t+1),      
        action_forward_str(t)       # action forward will not change the direction of the agent if it was in the north direction
        )
    
    # if agent currently heading towards the east, then the agent will turn left to face north
    left = "({0} & {1})".format(
        state_heading_east_str(t),
        action_turn_left_str(t)
        )
    
    # if agent currently heading towards the west, then the agent will turn right to face north
    right = "({0} & {1})".format(
        state_heading_west_str(t),
        action_turn_right_str(t)
        )

    return f"{heading_north_ssa} <=> ({action} | {left} | {right})"


"""
Name: Priyank Patel
"""
def axiom_generator_heading_east_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be East at time t+1

    t := time
    """
    heading_east_ssa = state_heading_east_str(t+1)
    action = "({0} & ({1} | {2} | {3} | {4} | {5}))".format(
        state_heading_east_str(t),      # the agent is already in the east direction at time t
        action_wait_str(t),             # action wait will not change the direction of the agent if it was in the east direction
        action_grab_str(t),             # action shoot will not change the direction of the agent if it was in the east direction
        action_shoot_str(t),            # action grab will not change the direction of the agent if it was in the east direction
        percept_bump_str(t+1),
        action_forward_str(t)           # action forward will not change the direction of the agent if it was in the east direction
        )
    
    # if agent currently heading towards the south, then the agent will turn left to face east
    left = "({0} & {1})".format(
        state_heading_south_str(t), 
        action_turn_left_str(t)
        )
    
    # if agent currently heading towards the north, then the agent will turn right to face east
    right = "({0} & {1})".format(
        state_heading_north_str(t), 
        action_turn_right_str(t)
        )
    
    return f"{heading_east_ssa} <=> ({action} | {left} | {right})"


"""
Name: Priyank Patel
"""
def axiom_generator_heading_south_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be South at time t+1

    t := time
    """
    heading_south_ssa = state_heading_south_str(t+1)
    action = "({0} & ({1} | {2} | {3} | {4} | {5}))".format(
        state_heading_south_str(t),     # the agent is already in the south direction at time t
        action_wait_str(t),             # action wait will not change the direction of the agent if it was in the south direction
        action_grab_str(t),             # action shoot will not change the direction of the agent if it was in the south direction
        action_shoot_str(t),            # action grab will not change the direction of the agent if it was in the south direction
        percept_bump_str(t+1),          
        action_forward_str(t)           # action forward will not change the direction of the agent if it was in the south direction
        )
    
    # if agent currently heading towards the west, then the agent will turn left to face south
    left = "({0} & {1})".format(
        state_heading_west_str(t),
        action_turn_left_str(t)
        )
    
    # if agent currently heading towards the east, then the agent will turn right to face south
    right = "({0} & {1})".format(
        state_heading_east_str(t),
        action_turn_right_str(t)
        ) 

    return f"{heading_south_ssa} <=> ({action} | {left} | {right})"


"""
Name: Priyank Patel
"""
def axiom_generator_heading_west_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be West at time t+1

    t := time
    """
    heading_west_ssa = state_heading_west_str(t+1)
    action = "({0} & ({1} | {2} | {3} | {4} | {5}))".format(
        state_heading_west_str(t),      # the agent is already in the west direction at time t
        action_wait_str(t),             # action wait will not change the direction of the agent if it was in the west direction
        action_grab_str(t),             # action shoot will not change the direction of the agent if it was in the west direction
        action_shoot_str(t),            # action grab will not change the direction of the agent if it was in the west direction
        percept_bump_str(t+1),          
        action_forward_str(t)           # action forward will not change the direction of the agent if it was in the west direction
        )
    
    # if agent currently heading towards the north, then the agent will turn left to face west
    left = "({0} & {1})".format(
        state_heading_north_str(t),
        action_turn_left_str(t)
        )
    
    # if agent currently heading towards the south, then the agent will turn right to face west
    right = "({0} & {1})".format(
        state_heading_south_str(t),
        action_turn_right_str(t)
        )
    
    return f"{heading_west_ssa} <=> ({action} | {left} | {right})"

def generate_heading_ssa(t):
    """
    Generates all of the heading SSAs.
    """
    return [axiom_generator_heading_north_ssa(t),
            axiom_generator_heading_east_ssa(t),
            axiom_generator_heading_south_ssa(t),
            axiom_generator_heading_west_ssa(t)]



def generate_non_location_ssa(t):
    """
    Generate all non-location-based SSAs
    """
    axioms = []  
    axioms.append(axiom_generator_have_arrow_ssa(t))
    axioms.append(axiom_generator_wumpus_alive_ssa(t))
    axioms.extend(generate_heading_ssa(t))
    return filter(lambda s: s != '', axioms)



#----------------------------------

"""
Name: Priyank Patel
"""
def axiom_generator_heading_only_north(t):
    """
    Assert that when heading is North, the agent is
    not heading any other direction.

    t := time
    """

    # if agent is heading only in north then the agent is not allowed heading go in any other direction
    north = state_heading_north_str(t)
    south = state_heading_south_str(t)
    east = state_heading_east_str(t)
    west = state_heading_west_str(t)
    axiom = f'{north} <=> ~({west} | {south} | {east})'
    return axiom

"""
Name: Priyank Patel
"""
def axiom_generator_heading_only_east(t):
    """
    Assert that when heading is East, the agent is
    not heading any other direction.

    t := time
    """
    # if agent is heading only in east then the agent is not allowed to heading in any other direction
    north = state_heading_north_str(t)
    south = state_heading_south_str(t)
    east = state_heading_east_str(t)
    west = state_heading_west_str(t)
    axiom = f'{east} <=> ~({north} | {south} | {west})'
    return axiom

"""
Name: Priyank Patel
"""
def axiom_generator_heading_only_south(t):
    """
    Assert that when heading is South, the agent is
    not heading any other direction.

    t := time
    """
    # if agent is heading only in north then the agent is not allowed to heading in any other direction
    north = state_heading_north_str(t)
    south = state_heading_south_str(t)
    east = state_heading_east_str(t)
    west = state_heading_west_str(t)
    axiom = f'{south} <=> ~({north} | {west} | {east})'
    return axiom


"""
Name: Priyank Patel
"""
def axiom_generator_heading_only_west(t):
    """
    Assert that when heading is West, the agent is
    not heading any other direction.

    t := time
    """
    
    # if agent is heading only in north then the agent is not allowed to heading in any other direction
    north = state_heading_north_str(t)
    south = state_heading_south_str(t)
    east = state_heading_east_str(t)
    west = state_heading_west_str(t)
    axiom = f'{west} <=> ~({north} | {south} | {east})'
    return axiom


def generate_heading_only_one_direction_axioms(t):
    return [axiom_generator_heading_only_north(t),
            axiom_generator_heading_only_east(t),
            axiom_generator_heading_only_south(t),
            axiom_generator_heading_only_west(t)]


"""
Name: Mujtaba jafri
"""
def axiom_generator_only_one_action_axioms(t):
    """
    Assert that only one axion can be executed at a time.

    t := time
    """
    actions = ['Forward', 'Grab', 'Shoot', 'Climb', 'TurnLeft', 'TurnRight', 'Wait']
    axioms_list = []
    for action in actions:
        other = ['~' + a + str(t) for a in actions if a != action]
        axioms_list.append("(" + action + str(t) + " <=> (" + (" & ".join(other)) + "))")


    return ' & '.join(axioms_list)



def generate_mutually_exclusive_axioms(t):
    """
    Generate all time-based mutually exclusive axioms.
    """
    axioms = []
    axioms.extend(generate_heading_only_one_direction_axioms(t + 1))
    axioms.append(axiom_generator_only_one_action_axioms(t))
    
    return filter(lambda s: s != '', axioms)

#-------------------------------------------------------------------------------
