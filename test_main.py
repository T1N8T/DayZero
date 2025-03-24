from main import main

def test_main(y_true_seconds:list,tol:float,modo:bool):
    
    y_prediction_seconds = main()
    if len(y_prediction_seconds) != len(y_true_seconds):
        raise ValueError("The length of the lists must be the same")
    individual_scores = []
    for y_prediction, y_true in zip(y_prediction_seconds, y_true_seconds, strict=True):
        delta = y_prediction - y_true
        if delta >= 0:
            score = pow(abs(delta), 2)
        else:
            score = pow(abs(delta), 1)
        individual_scores.append(score)
    final_score = sum(individual_scores)
    if modo:
        print(individual_scores)
    else:
        print(final_score)
    return final_score


