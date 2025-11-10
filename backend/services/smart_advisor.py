# backend/services/smart_advisor.py

import math

def rupees(n):
    """Formats a number into Indian currency format."""
    if n is None:
        return "₹0"
    s = f"{int(round(n)):,}"
    return "₹" + s.replace(",", ",")


class SmartAdvisor:
    """
    Converts underwriting numeric output into human-like advice.
    Helps explain best and chosen plans clearly.
    """

    def summarize(self, requested_amount, feasible_options, chosen, best):
        summary_lines = []

        chosen_emi = chosen["emi"]
        best_emi = best["emi"]
        diff_emi = abs(chosen_emi - best_emi)
        interest_saving = round(chosen["total_interest"] - best["total_interest"], 2)

        # 💬 Summary logic
        if chosen["tenure"] == best["tenure"]:
            summary_lines.append(
                f"Your chosen {chosen['tenure']}-month plan looks optimal for your requested amount."
            )
        elif chosen["tenure"] > best["tenure"]:
            summary_lines.append(
                f"You chose a longer {chosen['tenure']}-month tenure — it keeps EMI lower ({rupees(chosen_emi)}/month), "
                f"but total interest rises by about {rupees(interest_saving)} compared to the shorter {best['tenure']}-month option."
            )
        else:
            summary_lines.append(
                f"The {chosen['tenure']}-month option is more aggressive — EMI is {rupees(chosen_emi)}, "
                f"which is ₹{int(diff_emi)} different from the best balance plan."
            )

        # ⚖️ Affordability note
        if chosen["affordability"] < 30:
            summary_lines.append("Your EMI is well within a safe affordability range. ✅")
        elif chosen["affordability"] < 50:
            summary_lines.append("EMI is manageable but make sure you keep buffer for other expenses. 💡")
        else:
            summary_lines.append("EMI looks high — consider a longer tenure for comfort. ⚠️")

        # 🧾 Processing fee & interest
        summary_lines.append(
            f"Processing Fee: {rupees(chosen['processing_fee'])}, Total Interest: {rupees(chosen['total_interest'])}."
        )

        # 💡 Suggest better alternative if it exists
        if best["tenure"] != chosen["tenure"]:
            summary_lines.append(
                f"Alternative: {best['tenure']} months @ {best['rate']}% — EMI {rupees(best['emi'])}, saves about {rupees(interest_saving)} in interest."
            )

        return {
            "summary_lines": summary_lines,
            "chosen_tenure": chosen["tenure"],
            "best_tenure": best["tenure"],
            "chosen_rate": chosen["rate"],
            "best_rate": best["rate"],
            "emi_difference": diff_emi,
            "interest_saving": interest_saving,
        }