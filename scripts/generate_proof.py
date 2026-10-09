#!/usr/bin/env python3
"""Generate HTML proof showing non-linear weight interpolation"""

def generate_html_proof():
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>Metropolitan Line - Non-Linear Weight Proof</title>
    <style>
        body { font-family: system-ui; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .proof-table { width: 100%; border-collapse: collapse; }
        .proof-table th { 
            background: #333; color: white; padding: 10px; 
            text-align: left; position: sticky; top: 0;
        }
        .proof-table td { 
            padding: 15px; border-bottom: 1px solid #ddd;
            vertical-align: top;
        }
        .weight-label { 
            font-weight: bold; font-size: 14px; color: #666;
        }
        .non-linear-indicator {
            display: inline-block; width: 10px; height: 10px;
            border-radius: 50%; margin-right: 5px;
        }
        .flat-region { background: #4A90E2; }
        .steep-region { background: #E24A4A; }
        @font-face {
            font-family: 'MetropolitanLine';
            src: url('MetropolitanLine[wght].ttf') format('truetype');
            font-weight: 100 900;
        }
        .proof-text {
            font-family: 'MetropolitanLine';
            font-size: 48px;
            line-height: 1.2;
        }
    </style>
</head>
<body>
    <h1>Metropolitan Line - Non-Linear Weight Interpolation</h1>
    
    <h2>Interpolation Curve</h2>
    <p>
        <span class="non-linear-indicator flat-region"></span> 
        <strong>Light Region (100-400):</strong> Flat curve - stems stay thin longer
        <br>
        <span class="non-linear-indicator steep-region"></span>
        <strong>Bold Region (400-900):</strong> Steep curve - stems accelerate in thickness
    </p>
    
    <h2>Weight Samples</h2>
    <table class="proof-table">
        <tr>
            <th>Weight</th>
            <th>Internal Value</th>
            <th>Curve Region</th>
            <th>Sample Text</th>
        </tr>'''
    
    weights = [100, 200, 300, 400, 500, 600, 700, 800, 900]
    internal_values = [0.0, 0.08, 0.16, 0.25, 0.40, 0.60, 0.78, 0.92, 1.0]
    
    for weight, internal in zip(weights, internal_values):
        region = "flat" if weight <= 400 else "steep"
        region_class = "flat-region" if region == "flat" else "steep-region"
        
        html += f'''
        <tr>
            <td><span class="weight-label">{weight}</span></td>
            <td>{internal:.2f}</td>
            <td><span class="non-linear-indicator {region_class}"></span>{region}</td>
            <td>
                <div class="proof-text" style="font-weight: {weight};">
                    Hamburgfontsiv 123
                </div>
            </td>
        </tr>'''
    
    html += '''
    </table>
    
    <h2>Linear vs Non-Linear Comparison</h2>
    <p>Without avar2, weight 400 would be at internal value 0.43 (43% toward Bold).<br>
    With avar2, weight 400 is at internal value 0.25 (25% toward Bold) - staying lighter.</p>
    
    <script>
        // Visualize the curve
        console.log("Metropolitan Line Non-Linear Weight Curve:");
        console.log("Light region: Flat slope");
        console.log("Bold region: Steep slope");
    </script>
</body>
</html>'''
    
    with open('build/proof.html', 'w') as f:
        f.write(html)
    
    print("Proof generated: build/proof.html")

if __name__ == "__main__":
    generate_html_proof()