#!/usr/bin/env python3
"""
Standalone script for analyzing backtest results and generating insights.
This script can analyze results from previous backtests and provide detailed analysis.
"""

import sys
import os
import json
sys.path.append('.')

def main():
    """Analyze backtest results and generate comprehensive insights."""
    print("🔍 Trading Backtester - Results Analysis")
    print("=" * 50)
    
    try:
        from analysis.visualizer import Visualizer
        from analysis.performance_analyzer import PerformanceAnalyzer
        
        # Check if results file exists
        results_file = "backtest_results.json"
        if not os.path.exists(results_file):
            print(f"❌ Results file '{results_file}' not found.")
            print("Please run a backtest first to generate results.")
            return False
        
        # Load results
        print(f"📂 Loading results from {results_file}...")
        with open(results_file, 'r') as f:
            results = json.load(f)
        print("✓ Results loaded successfully")
        
        # Initialize analyzer and visualizer
        analyzer = PerformanceAnalyzer()
        visualizer = Visualizer()
        
        # Generate comprehensive analysis
        print("\n📊 Generating comprehensive analysis...")
        analysis_report = visualizer.generate_analysis_report(results)
        
        # Display analysis
        print("\n" + "="*60)
        print(analysis_report)
        print("="*60)
        
        # Save analysis to file
        analysis_file = "detailed_analysis_report.txt"
        with open(analysis_file, 'w') as f:
            f.write(analysis_report)
        
        print(f"\n📄 Detailed analysis saved to: {analysis_file}")
        
        # Generate additional insights
        print("\n🔍 ADDITIONAL INSIGHTS")
        print("-" * 20)
        
        metrics = results['metrics']
        trades = results['trades']
        
        # Strategy performance insights
        total_return = metrics.get('total_return', 0)
        sharpe_ratio = metrics.get('sharpe_ratio', 0)
        max_drawdown = metrics.get('max_drawdown', 0)
        
        print(f"📈 Strategy Performance Insights:")
        print(f"   • Total Return: {total_return:.2%}")
        print(f"   • Risk-Adjusted Return (Sharpe): {sharpe_ratio:.3f}")
        print(f"   • Maximum Drawdown: {max_drawdown:.2%}")
        
        # Trading behavior insights
        if trades:
            print(f"\n📊 Trading Behavior Insights:")
            print(f"   • Total Trades: {len(trades)}")
            print(f"   • Average Trade P&L: ${metrics.get('avg_trade_pnl', 0):,.2f}")
            print(f"   • Win Rate: {metrics.get('win_rate', 0):.2%}")
            print(f"   • Profit Factor: {metrics.get('profit_factor', 0):.3f}")
            
            # Analyze trade distribution
            winning_trades = [t for t in trades if t['pnl'] > 0]
            losing_trades = [t for t in trades if t['pnl'] < 0]
            
            if winning_trades and losing_trades:
                avg_win = sum(t['pnl'] for t in winning_trades) / len(winning_trades)
                avg_loss = sum(t['pnl'] for t in losing_trades) / len(losing_trades)
                print(f"   • Average Win: ${avg_win:,.2f}")
                print(f"   • Average Loss: ${avg_loss:,.2f}")
                print(f"   • Win/Loss Ratio: {abs(avg_win/avg_loss):.2f}")
        
        # Risk management insights
        print(f"\n🛡️  Risk Management Insights:")
        if abs(max_drawdown) > 0.2:
            print(f"   ⚠️  High drawdown detected - consider position sizing adjustments")
        else:
            print(f"   ✅ Drawdown within acceptable limits")
        
        if sharpe_ratio < 1.0:
            print(f"   ⚠️  Low risk-adjusted returns - consider strategy optimization")
        else:
            print(f"   ✅ Good risk-adjusted returns")
        
        # Market condition insights
        if 'volatility' in metrics:
            volatility = metrics['volatility']
            print(f"\n🌍 Market Condition Insights:")
            print(f"   • Portfolio Volatility: {volatility:.2%}")
            if volatility > 0.3:
                print(f"   ⚠️  High volatility period - strategy may be more risky")
            elif volatility < 0.15:
                print(f"   ✅ Low volatility period - stable trading conditions")
            else:
                print(f"   ✅ Moderate volatility - typical market conditions")
        
        # Actionable recommendations
        print(f"\n💡 ACTIONABLE RECOMMENDATIONS:")
        print("-" * 30)
        
        recommendations = []
        
        if total_return < 0.05:
            recommendations.append("• Consider testing different strategy parameters")
            recommendations.append("• Review market conditions during the test period")
        
        if sharpe_ratio < 0.8:
            recommendations.append("• Implement better risk management rules")
            recommendations.append("• Consider reducing position sizes")
        
        if len(trades) < 30:
            recommendations.append("• Test over longer time periods for more reliable results")
            recommendations.append("• Consider adjusting signal frequency")
        
        if not recommendations:
            recommendations.append("• Strategy shows good performance - consider live trading with small positions")
            recommendations.append("• Continue monitoring performance across different market conditions")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📁 Files generated:")
        print(f"   - {analysis_file} (detailed analysis)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
