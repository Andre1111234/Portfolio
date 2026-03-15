import sys
import config
from analytics import Research, Analytics

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 make_report.py <file_path>")
        sys.exit(1)
    
    research = Research(sys.argv[1])
    
    try:
        data = research.file_reader()
        
        analytics = Analytics(data)
        heads, tails = analytics.counts()
        head_frac, tail_frac = analytics.fractions(heads, tails)
        
        random_predictions = analytics.predict_random(config.num_of_steps)
        forecast_heads = sum(pred[0] for pred in random_predictions)
        forecast_tails = sum(pred[1] for pred in random_predictions)
        
        report = config.report_template.format(
            total_observations=len(data),
            tails=tails,
            heads=heads,
            tail_prob=tail_frac * 100,
            head_prob=head_frac * 100,
            num_steps=config.num_of_steps,
            tail_forecast=forecast_tails,
            head_forecast=forecast_heads
        )
        
        analytics.save_file(report, "report", "txt")
        research.send_telegram_message(success=True)
        print("Report has been successfully created and saved to report.txt")
        
    except Exception as e:
        print(f"Error: {e}")
        research.send_telegram_message(success=False)
        sys.exit(1)

if __name__ == '__main__':
    main()