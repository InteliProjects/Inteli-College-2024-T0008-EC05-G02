import React from 'react';
import { Button } from 'antd';
import './Norepinefrina.jpg';
import './style.css';
import remedio from './Norepinefrina.jpg';
import DrugCard from '../../components/drugCard';

function MedicamentoConformidade() {
  return (
    <div className="conformidade">
    <h1 className="title">Em Criação...</h1>
        <DrugCard 
        color="green" 
        status="em conformidade" 
        image={remedio} 
        name="Norepinefrina"
        dose="5mg"
        expiration="01/10/2024  "
        batch="A2023"
        supplier="NovaFarma"
        />
    {/* </div> */}
    <div className="card-footer">
        <Button type="primary" className="pause-button">Pausar Bipagem</Button>
        <Button type="danger" className="finish-button">Finalizar Bipagem</Button>
      </div>
 </div>
  );
}

export default MedicamentoConformidade;
