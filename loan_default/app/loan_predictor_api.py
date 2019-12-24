#----------------------------Loan Default Prediction--------------------------#
import pandas as pd
import sys
from flask import Flask,request,jsonify,Blueprint
from flask_cors import CORS
from flask_restplus import Resource,Api,fields,reqparse
import traceback
import joblib
import pickle
app=Flask(__name__)
blueprint = Blueprint('api',__name__, url_prefix='/loan')
api = Api(blueprint,
          version='1.1.3',
          title='Loan Default API',
          default='Loan Default',
          default_label='',
          doc='/')

app.register_blueprint(blueprint)

CORS(app)
input_data = api.model('Loan_Default_Input', {
    'dependents': fields.Integer(required=True,example=2),
    'credit_history': fields.Integer(required=True,example= 1.0),
    'applicantIncome': fields.Float(required=True,example=4000),
    'coapplicantIncome': fields.Float(required=True,example=2000),
    'loanAmount': fields.Float(required=True,exapmle=200),
    'loan_Amount_Term':fields.Integer(required =True,example=180),
    'gender':fields.String(required =True,example='Male'),
    'married':fields.String(required =True,example='Yes'),
    'education':fields.String(required=True,example='Graduate'),
    'self_Employed':fields.String(required=True,example='Yes'),
    'property_Area':fields.String(required=True,example='Urban'),
})

pagination=reqparse.RequestParser()
pagination.add_argument('x',type=int,required=True,default=1,help='x value')
pagination.add_argument('y',type=int,required=True,default=1,help='y value')
@api.route('/predict')
class product_reco(Resource):
    def get(self):
        return 'loan_default_prediction'
    @api.doc(id='get something')
    @api.expect(input_data)
    def post(self):
        if model:
            try:
                input_json=api.payload
                df=pd.DataFrame([input_json])
                df.columns=['Dependents','Credit_History','ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Gender','Married','Education','Self_Employed','Property_Area']
                df = df.reindex(columns = cols, fill_value = 0)
                df = df.astype(col_dtypes)
                X = encoder.transform(df[cat_var])
                query_enc = pd.DataFrame(X, columns=enc_cols, index=df.index, dtype='int8')
                query_new = pd.concat([df[list(num_cols)], query_enc], axis =1)
            
                prediction =model.predict_proba(query_new).tolist()
            
                res={'probability':prediction[0][0]}
                return jsonify(res)
            except:
                return jsonify({'trace': traceback.format_exc()})
        else:
            print('Train the model first')
            return ('No model here to use')


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = 5000	
    with open(r'cols.pkl', 'rb') as f:
        cols = pickle.load(f)
	
    with open(r'enc_cols.pkl','rb') as f:
        enc_cols=pickle.load(f)
      
    with open(r'cols_dtypes.pkl', 'rb') as f:
        col_dtypes = pickle.load(f)
    
    cat_var = joblib.load(r'cat_var.pkl')
    num_cols = joblib.load(r'num_cols.pkl')
    
    with open(r'loan_default_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    print ('Model loaded')
    encoder = joblib.load(r'encoder.pkl')
    print('Encoder loaded')
    app.run(host='0.0.0.0',port = port,debug=True)

