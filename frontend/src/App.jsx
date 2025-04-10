import { useState } from 'react';

const App = () => {
  const [formData, setFormData] = useState({
    age: '',
    weight: '',
    height: '',
    bmi: '',
    waist_hip_ratio: '',
    cycle: 'R',
    cycle_length: '',
    hair_growth: 'no',
    weight_gain: 'no',
    pimples: 'no',
    hair_loss: 'no',
    skin_darkening: 'no',
    fast_food: 0,
    exercise: 'no',

    // Hormonal profile toggle + fields
    hasHormonalReport: 'no',
    lh: '',
    fsh: '',
    amh: '',
    tsh: '',
    prl: '',
    vit_d3: '',

    // Ultrasound toggle + fields
    hasUltrasound: 'no',
    avg_f_size_l: '',
    follicle_no_l: '',
    avg_f_size_r: '',
    follicle_no_r: '',
    endometrium: '',
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-3xl border-purple-700">
        <h1 className="text-3xl font-bold mb-6 text-center text-purple-700">✨ PCOS Prediction Form</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* General Inputs */}
          {[
            ['Age (yrs)', 'age'],
            ['Weight (Kg)', 'weight'],
            ['Height (Cm)', 'height'],
            ['BMI (optional)', 'bmi'],
            ['Waist:Hip Ratio', 'waist_hip_ratio'],
            ['Cycle length (days)', 'cycle_length'],
            ['Fast food intake (times/week)', 'fast_food']
          ].map(([label, name]) => (
            <div key={name}>
              <label className="block text-gray-700">{label}</label>
              <input
                name={name}
                value={formData[name]}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border rounded-md shadow-sm"
              />
            </div>
          ))}

          {/* Menstrual Cycle */}
          <div>
            <label className="block text-gray-700">Menstrual Cycle</label>
            <select
              name="cycle"
              value={formData.cycle}
              onChange={handleChange}
              className="w-full mt-1 p-2 border rounded-md shadow-sm"
            >
              <option value="R">Regular</option>
              <option value="I">Irregular</option>
            </select>
          </div>

          {[
            ['Hair growth on face/chest?', 'hair_growth'],
            ['Weight gain?', 'weight_gain'],
            ['Pimples?', 'pimples'],
            ['Hair loss?', 'hair_loss'],
            ['Skin darkening?', 'skin_darkening'],
            ['Exercise regularly?', 'exercise'],
          ].map(([label, name]) => (
            <div key={name}>
              <label className="block text-gray-700">{label}</label>
              <select
                name={name}
                value={formData[name]}
                onChange={handleChange}
                className="w-full mt-1 p-2 border rounded-md shadow-sm"
              >
                <option value="yes">Yes</option>
                <option value="no">No</option>
              </select>
            </div>
          ))}

          {/* Hormonal Report Section */}
          <div>
            <label className="block text-gray-700">Do you have a recent Hormonal Report?</label>
            <select
              name="hasHormonalReport"
              value={formData.hasHormonalReport}
              onChange={handleChange}
              className="w-full mt-1 p-2 border rounded-md"
            >
              <option value="no">No</option>
              <option value="yes">Yes</option>
            </select>
          </div>

          {formData.hasHormonalReport === 'yes' && (
            <>
              {[
                ['LH (Luteinizing Hormone)', 'lh'],
                ['FSH (Follicle Stimulating Hormone)', 'fsh'],
                ['AMH (Anti-Müllerian Hormone)', 'amh'],
                ['TSH (Thyroid Stimulating Hormone)', 'tsh'],
                ['PRL (Prolactin)', 'prl'],
                ['Vitamin D3 level', 'vit_d3'],
              ].map(([label, name]) => (
                <div key={name}>
                  <label className="block text-gray-700">{label}</label>
                  <input
                    name={name}
                    value={formData[name]}
                    onChange={handleChange}
                    className="w-full mt-1 p-2 border rounded-md"
                  />
                </div>
              ))}
            </>
          )}

          {/* Ultrasound Section */}
          <div>
            <label className="block text-gray-700">Do you have Ultrasound Data?</label>
            <select
              name="hasUltrasound"
              value={formData.hasUltrasound}
              onChange={handleChange}
              className="w-full mt-1 p-2 border rounded-md"
            >
              <option value="no">No</option>
              <option value="yes">Yes</option>
            </select>
          </div>

          {formData.hasUltrasound === 'yes' && (
            <>
              {[
                ['Average follicle size in left ovary (mm)', 'avg_f_size_l'],
                ['Follicles in left ovary', 'follicle_no_l'],
                ['Average follicle size in right ovary (mm)', 'avg_f_size_r'],
                ['Follicles in right ovary', 'follicle_no_r'],
                ['Endometrium thickness (mm)', 'endometrium'],
              ].map(([label, name]) => (
                <div key={name}>
                  <label className="block text-gray-700">{label}</label>
                  <input
                    name={name}
                    value={formData[name]}
                    onChange={handleChange}
                    className="w-full mt-1 p-2 border rounded-md"
                  />
                </div>
              ))}
            </>
          )}

          <button
            type="submit"
            className="w-full bg-purple-600 text-white py-2 rounded-md hover:bg-purple-700 transition"
          >
            Predict
          </button>
        </form>

        {result && (
          <div className="mt-8 bg-gray-50 p-4 rounded-md shadow-inner">
            <h2 className="text-xl font-semibold mb-2">🔍 Prediction Result</h2>
            <p>📊 <strong>Risk Probability:</strong> {result.risk_percent}%</p>
            <p>⚠️ <strong>Risk Level:</strong> {result.risk_level}</p>
            <p>{result.message}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
