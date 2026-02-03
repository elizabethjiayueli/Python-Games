Here's a revised program that only gives money for grades in the 90% range (A-, A, A+), with realistic middle school appropriate rewards:

```python
class GradeRewardCalculator:
    def __init__(self):
        self.grades = []
        self.subjects = []
        self.paying_grades = ['A-', 'A', 'A+']  # Only these grades earn money
        self.base_rewards = {
            'A+': 15.00,  # 97-100% equivalent
            'A': 12.00,   # 93-96% equivalent
            'A-': 10.00,  # 90-92% equivalent
            'B+': 0.00,   # 87-89%
            'B': 0.00,    # 83-86%
            'B-': 0.00,   # 80-82%
            'C+': 0.00,   # 77-79%
            'C': 0.00,    # 73-76%
            'C-': 0.00,   # 70-72%
            'D': 0.00,    # 60-69%
            'F': 0.00     # Below 60%
        }
        
        self.grade_percentages = {
            'A+': "97-100%",
            'A': "93-96%",
            'A-': "90-92%",
            'B+': "87-89%",
            'B': "83-86%",
            'B-': "80-82%",
            'C+': "77-79%",
            'C': "73-76%",
            'C-': "70-72%",
            'D': "60-69%",
            'F': "Below 60%"
        }
    
    def get_valid_grade(self):
        """Get a valid grade input from the user"""
        valid_grades = list(self.base_rewards.keys())
        
        while True:
            print(f"\nGrade Options:")
            for grade, percentage in self.grade_percentages.items():
                print(f"  {grade}: {percentage}")
            
            grade = input("\nEnter grade letter: ").upper()
            if grade in valid_grades:
                return grade
            else:
                print(f"❌ Invalid grade. Please choose from the options above.")
    
    def input_grades(self):
        """Allow user to input multiple grades"""
        print("=" * 60)
        print("🎓 ACHIEVEMENT REWARD CALCULATOR")
        print("=" * 60)
        print("\n📝 ONLY grades 90% and above (A-, A, A+) earn money!")
        print("   A- = $10.00  |  A = $12.00  |  A+ = $15.00")
        print("   All other grades earn $0.00\n")
        
        subject_number = 1
        while True:
            print(f"\n{'='*40}")
            print(f"Subject #{subject_number}")
            subject = input("Enter subject name (or 'done' to finish): ").strip()
            
            if subject.lower() == 'done':
                if len(self.grades) == 0:
                    print("⚠️  Please enter at least one grade!")
                    continue
                break
            
            grade = self.get_valid_grade()
            
            self.subjects.append(subject)
            self.grades.append(grade)
            subject_number += 1
    
    def calculate_rewards(self):
        """Calculate total, spending, and saving money"""
        total_reward = 0
        honor_roll_count = 0
        
        print("\n" + "=" * 60)
        print("📊 GRADE REPORT CARD")
        print("=" * 60)
        
        # Display individual grades and rewards
        for i, (subject, grade) in enumerate(zip(self.subjects, self.grades), 1):
            reward = self.base_rewards[grade]
            total_reward += reward
            
            if grade in self.paying_grades:
                print(f"{i}. {subject:15} → {grade:3} ({self.grade_percentages[grade]}) = 💲{reward:5.2f} ✅ EARNED!")
                honor_roll_count += 1
            else:
                print(f"{i}. {subject:15} → {grade:3} ({self.grade_percentages[grade]}) = 💲{reward:5.2f} ❌ No reward")
        
        # Calculate percentage of A grades
        if len(self.grades) > 0:
            honor_roll_percentage = (honor_roll_count / len(self.grades)) * 100
        else:
            honor_roll_percentage = 0
        
        # Bonus for getting all A's
        bonus = 0
        if honor_roll_count == len(self.grades) and honor_roll_count > 0:
            bonus = 20.00
            total_reward += bonus
            print(f"\n🎉 EXTRA BONUS: All subjects 90%+ = +${bonus:.2f}!")
        
        return total_reward, honor_roll_count, honor_roll_percentage
    
    def display_results(self, total, honor_roll_count, honor_roll_percentage):
        """Display the results in a user-friendly way"""
        print("\n" + "=" * 60)
        print("💰 REWARD BREAKDOWN")
        print("=" * 60)
        
        print(f"\n📈 ACADEMIC ACHIEVEMENT:")
        print(f"   • Total Subjects: {len(self.grades)}")
        print(f"   • Honor Roll Subjects (90%+): {honor_roll_count}")
        print(f"   • Honor Roll Percentage: {honor_roll_percentage:.1f}%")
        
        print(f"\n💵 TOTAL EARNED: ${total:.2f}")
        
        if total > 0:
            # Calculate spending and saving (75% for spending, 25% for saving)
            spending_money = total * 0.75
            saving_money = total * 0.25
            
            print("\n💸 SPENDING MONEY (75%):")
            print(f"   ${spending_money:.2f}")
            print("   You could buy:")
            print(f"   • {int(spending_money // 3)} school lunches or snacks")
            print(f"   • {int(spending_money // 15)} movie tickets")
            print(f"   • {int(spending_money // 25)} video game (on sale)")
            print(f"   • {int(spending_money // 10)} books or school supplies")
            
            print("\n🏦 SAVINGS MONEY (25%):")
            print(f"   ${saving_money:.2f}")
            print("   Future value:")
            print(f"   • 1 year: ${saving_money * 1.03:.2f} (3% interest)")
            print(f"   • 5 years: ${saving_money * 1.16:.2f} (with regular savings)")
            
            # Goal suggestions
            print("\n🎯 NEXT GOAL:")
            next_target = (honor_roll_count + 1) * 12  # Average A grade value
            if honor_roll_count < len(self.grades):
                print(f"   Get {len(self.grades) - honor_roll_count} more subject(s) to 90%+")
                print(f"   Potential additional earnings: ${next_target:.2f}")
        else:
            print("\n💡 NO REWARDS EARNED THIS TIME")
            print("   Focus on getting at least 90% in your next subjects!")
            print("   Remember: A- (90-92%) earns $10.00!")
            
            # Motivation for next time
            potential_reward = len(self.grades) * 10  # Minimum A- value
            print(f"\n   💪 If ALL subjects reach 90%+ next time:")
            print(f"      You could earn: ${potential_reward:.2f} + $20 bonus = ${potential_reward + 20:.2f}!")
    
    def generate_study_plan(self):
        """Create a study plan based on current grades"""
        low_grades = []
        for subject, grade in zip(self.subjects, self.grades):
            if grade not in self.paying_grades:
                low_grades.append((subject, grade))
        
        if low_grades:
            print("\n" + "=" * 60)
            print("📚 SUGGESTED STUDY PLAN")
            print("=" * 60)
            
            for subject, grade in low_grades:
                needed_improvement = ""
                if grade in ['B+', 'B', 'B-']:
                    needed_improvement = " (Need 1-10 more percentage points)"
                elif grade in ['C+', 'C', 'C-']:
                    needed_improvement = " (Need 10-20 more percentage points)"
                elif grade in ['D', 'F']:
                    needed_improvement = " (Need 20+ percentage points - ask for help!)"
                
                print(f"\n• {subject}: Currently {grade} → Aim for A-")
                print(f"  {self.grade_percentages[grade]} → {self.grade_percentages['A-']}{needed_improvement}")
            
            print(f"\n💡 STUDY TIPS:")
            print("  • Spend 30 extra minutes daily on challenging subjects")
            print("  • Ask teachers for specific improvement areas")
            print("  • Form a study group with classmates")
            print("  • Review material 10 minutes every day")
    
    def save_to_file(self, total, honor_roll_count, honor_roll_percentage):
        """Save the results to a file"""
        try:
            import datetime
            
            filename = "academic_rewards.txt"
            with open(filename, 'w') as f:
                f.write("=" * 50 + "\n")
                f.write("ACADEMIC ACHIEVEMENT REPORT\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("GRADES:\n")
                f.write("-" * 30 + "\n")
                for subject, grade in zip(self.subjects, self.grades):
                    earned = "✓ PAID" if grade in self.paying_grades else "✗ NO REWARD"
                    f.write(f"{subject:15} : {grade:3} = {earned}\n")
                
                f.write(f"\nSUMMARY:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Total Subjects: {len(self.grades)}\n")
                f.write(f"Honor Roll Subjects (90%+): {honor_roll_count}\n")
                f.write(f"Honor Roll Percentage: {honor_roll_percentage:.1f}%\n")
                f.write(f"Total Earned: ${total:.2f}\n")
                
                if total > 0:
                    f.write(f"Spending Money (75%): ${total * 0.75:.2f}\n")
                    f.write(f"Savings (25%): ${total * 0.25:.2f}\n")
                
                f.write(f"\nReport generated: {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                f.write("=" * 50 + "\n")
            
            print(f"\n📁 Report saved to '{filename}'")
        except Exception as e:
            print(f"\n⚠️  Could not save report: {e}")

def main():
    print("🎯 EXCELLENCE REWARDS PROGRAM 🎯")
    print("\n" + "=" * 60)
    print("REWARD RULES:")
    print("  ✅ A- (90-92%) = $10.00")
    print("  ✅ A  (93-96%) = $12.00")
    print("  ✅ A+ (97-100%) = $15.00")
    print("  ✅ BONUS: All subjects 90%+ = $20.00 extra!")
    print("  ❌ All other grades = $0.00")
    print("=" * 60)
    
    while True:
        calculator = GradeRewardCalculator()
        
        # Input grades
        calculator.input_grades()
        
        # Calculate rewards
        total, honor_roll_count, honor_percentage = calculator.calculate_rewards()
        
        # Display results
        calculator.display_results(total, honor_roll_count, honor_percentage)
        
        # Generate study plan if needed
        if honor_roll_count < len(calculator.grades):
            calculator.generate_study_plan()
        
        # Save results
        save_choice = input("\n📝 Save this report to file? (yes/no): ").lower()
        if save_choice.startswith('y'):
            calculator.save_to_file(total, honor_roll_count, honor_percentage)
        
        print("\n" + "=" * 60)
        print("🏆 STRIVE FOR EXCELLENCE!")
        print("=" * 60)
        
        # Offer to calculate again
        again = input("\nCalculate another set of grades? (yes/no): ").lower()
        if not again.startswith('y'):
            print("\n🎓 Keep up the great work! Academic success pays off!")
            break
        
        print("\n" * 2)

if __name__ == "__main__":
    main()


Key Features of this 90%+ Reward System:

Reward Structure:

· A+ (97-100%) = $15.00
· A (93-96%) = $12.00
· A- (90-92%) = $10.00
· All other grades (B+ and below) = $0.00
· Bonus: All subjects 90%+ = $20.00 extra!

Financial Education:

· 75% Spending Money - For immediate rewards
· 25% Savings - Teaches long-term financial planning
· Shows what spending money can buy
· Demonstrates savings growth over time

Motivational Features:

· Clear percenta