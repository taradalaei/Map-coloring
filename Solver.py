from collections import deque
from typing import Callable, List, Tuple
from CSP import CSP


class Solver(object):

    def __init__(self, csp: CSP, domain_heuristics: bool = False, variable_heuristics: bool = False, AC_3: bool = False) -> None:
        """
        Initializes a Solver object.

        Args:
            csp (CSP): The Constraint Satisfaction Problem to be solved.
            domain_heuristics (bool, optional): Flag indicating whether to use domain heuristics. Defaults to False.
            variable_heuristics (bool, optional): Flag indicating whether to use variable heuristics. Defaults to False.
            AC_3 (bool, optional): Flag indicating whether to use the AC-3 algorithm. Defaults to False.
        """
        self.domain_heuristic = domain_heuristics
        self.variable_heuristic = variable_heuristics
        self.AC_3 = AC_3
        self.csp = csp


    def backtrack_solver(self) -> List[Tuple[str, str]]:
        """
        Backtracking algorithm to solve the constraint satisfaction problem (CSP).

        Returns:
            List[Tuple[str, str]]: A list of variable-value assignments that satisfy all constraints.
        """

        "*** YOUR CODE HERE ***"
        def backtrack(assignment):
            if self.csp.is_complete():
                return assignment

            var = self.select_unassigned_variable()

            for value in self.ordered_domain_value(var):
                if self.csp.is_consistent(var, value):
                    self.csp.assign(var, value)
                    assignment.append((var, value))

                    result = backtrack(assignment)
                    if result is not None:
                        return result 

                    self.csp.unassign(self.csp.domain, var)
            return None  

        return backtrack([])


    def select_unassigned_variable(self) -> str:
        """
        Selects an unassigned variable using the MRV heuristic.

        Returns:
            str: The selected unassigned variable.
        """
        if self.variable_heuristic:
            return self.MRV()
        return self.csp.unassigned_var[0]

    def ordered_domain_value(self, variable: str) -> List[str]:
        """
        Returns a list of domain values for the given variable in a specific order.

        Args:
            variable (str): The name of the variable.

        Returns:
            List[str]: A list of domain values for the variable in a specific order.
        """
        # Function implementation goes here
        if self.domain_heuristic:
            return self.LCV(variable)
        return self.csp.variables[variable]

        

    def arc_reduce(self, x, y, consistent) -> List[str]:
        """
        Reduce the domain of variable x based on the constraints between x and y.

        Parameters:
        - x: The first variable.
        - y: The second variable.
        - consistent: A function that checks the consistency between two values.

        Returns:
        - The reduced domain of variable x if the domain is reduced, None otherwise.
        """
        "*** YOUR CODE HERE ***"
        domain_reduced = False
        domain_x = self.csp.variables[x]
        domain_y = self.csp.variables[y]

        revised = False

        for value_x in domain_x:
            consistent_with_y = any(consistent(value_x, value_y) for value_y in domain_y)
            if not consistent_with_y:
                self.csp.variables[x].remove(value_x)
                domain_reduced = True
                revised = True

        if revised:
            if not domain_x: 
                return None #We have no solution

        return domain_x if domain_reduced else None


    def apply_AC3(self) -> List[Tuple[str, str]]:
        """
        Applies the AC3 algorithm to reduce the domains of variables in the CSP.

        Returns:
            A list of tuples representing the removed values from the domain of variables.
        """
        "*** YOUR CODE HERE ***"
        removed_values = []
        queue = deque([(xi, xj) for xi in self.csp.variables for xj in self.csp.var_constraints[xi]])   #Get all arcs in a queue

        while queue:
            xi, xj = queue.popleft()
            if self.arc_reduce(xi, xj, self.csp.constraint_func):
                if not self.csp.variables[xi]:
                    return None  # Domain is empty so no solution
                for xk in self.csp.var_constraints[xi]:   #To check other variables(xk) which are neighbors of xi that xi and it's neighbors are still consistent due to the reduction domain of xi and to see if we need any further domain reduction. 
                    if xk != xj:                            #We do not wann check xj again
                        queue.append((xk, xi))          #In order to check we add them to our queue
                removed_values.append((xi, xj))

        return removed_values
        

    def MRV(self) -> str:
        """
        Selects the variable with the Minimum Remaining Values (MRV) heuristic.

        Returns:
            str: The variable with the fewest remaining values.
        """
        "*** YOUR CODE HERE ***"
        min_remaining_values = 1000
        selected_variable = None

        for variable in self.csp.unassigned_var:
            remaining_values = len(self.csp.variables[variable])
            if(remaining_values <= min_remaining_values):
                min_remaining_values = remaining_values
                selected_variable = variable
        
        return selected_variable



    def LCV(self, variable: str) -> List[str]:
        """
        Orders the values of a variable based on the Least Constraining Value (LCV) heuristic.

        Args:
            variable (str): The variable for which to order the values.

        Returns:
            List[str]: A list of values sorted based on the number of constraints they impose.
        """
        "*** YOUR CODE HERE ***"
        constraints_count = {value: 0 for value in self.csp.variables[variable]} #their key are the variables values and their values are their constraints count


        for value in self.csp.variables[variable]:
            for neighbor in self.csp.var_constraints[variable]:
                if value in self.csp.variables[neighbor]:
                    constraints_count[value] += 1

        # a sorted list of values of variable sorted based on the count of their constraints
        sorted_values = sorted(constraints_count, key=lambda x: constraints_count[x])

        return sorted_values
