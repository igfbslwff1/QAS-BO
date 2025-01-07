# Convert clauses into ordinary logical formulas
def clause_to_logic(clause):
    logic_clause = "("
    for literal in clause:
        if literal > 0:
            logic_clause += f"x{literal} OR "
        else:
            logic_clause += f"NOT x{-literal} OR "
    logic_clause = logic_clause[:-4] + ")"  # Remove the last "OR"
    return logic_clause

def logic_expression(easy_clauses):
    # Make the whole formula
    logic_expression = " AND ".join([clause_to_logic(clause) for clause in easy_clauses])

    # Output result
    print("\nLogic expression:")
    print(logic_expression)
    print()