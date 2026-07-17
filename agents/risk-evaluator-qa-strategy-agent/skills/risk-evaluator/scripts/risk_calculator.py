import sys
import json

def calculate_risk(impact, complexity):
    """
    Compute the risk based on business impact and technical complexity.
    Scale: 1 to 5
    """
    # Formula defined in the specification: (Impact * 70%) + (Complexity * 30%)
    score = (impact * 0.7) + (complexity * 0.3)
    
    if score >= 4.5:
        level = "Critical"
    elif score >= 3.5:
        level = "High"
    elif score >= 2.5:
        level = "Medium"
    else:
        level = "Low"
        
    return round(score, 2), level

if __name__ == "__main__":
    # Simulation of input from Skill 1 (you can pass arguments by CLI)
    try:
        # Example: python risk_calculator.py 5 4
        imp = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
        comp = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
        
        final_score, final_level = calculate_risk(imp, comp)
        
        result = {
            "raw_score": final_score,
            "severity_level": final_level,
            "status": "success"
        }
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))