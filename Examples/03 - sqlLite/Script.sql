--
-- Esempio 1: Voglio l’elenco di tutti i test (tabella simbio_test) presenti nel mio DB.
SELECT * FROM simbio_test;
--
-- Esempio 2: dalla lista precedente voglio solo il nome e tempo di inizio e fine
SELECT st.testName, st.start, st.stop FROM simbio_test st;
--
-- Esempio 3: le stesse info dell’esempio 2 ma solo quelli eseguiti il 11/12/2018
SELECT st.testName, st.start, st.stop FROM simbio_test st WHERE st.start > "2018-12-11 00:00:00" AND st.stop < "2018-12-11 23:59:59";
--
-- Esempio 4: Voglio tutti i campi delle sottofasi della fase “CRUISE” ordinati cronologicamente (sapendo che fase e sottofase sono collegati tramite un id):
SELECT sp.* FROM simbio_subphase sp, simbio_phase p WHERE p.id = sp.lpName_id AND p.sName = "CRUISE" ORDER BY sp.start;
--
-- Esercizio: Selezionare il primo telecomando di scienza di VIHI eseguito l’11/12/2018 e fornire il tempo a cui è stato eseguito e tempo di integrazione.
--
-- Seleziono l'id del primo telecomando contenete nella descrizione la stringa "VIHI science" nel tabella dei telecomandi
SELECT id FROM simbio_telecommand tc WHERE tc.tcDescription LIKE "%VIHI science%" LIMIT 1; 
-- Seleziono il tempo di esecuzione e l'id all'inteno della tabella delle sequenze fissando l'id trovato in precedenza e restringendo il 
-- campo all'intevallo di tempo desiderato. Ottengo così il primo dato della mia ricerca
SELECT executionTime, id  FROM simbio_tcseq  WHERE simbio_tcseq.tcName_id=306 AND executionTime > "2018-12-11 00:00:00" AND executionTime < "2018-12-12 23:59:59" LIMIT 1;
-- Seleziono dalla tabella dei parametri l'id del paramentro che contiene nella descrizione la stringa "VIHI integration"
SELECT id FROM simbio_tcparameter WHERE parDescription LIKE "%VIHI integration%";
-- Seleziono il valore che assume il parametro nella sequenza cercata
SELECT value FROM simbio_tcdetail WHERE sec_id=9784 AND parName_id=578;
-- Equivalente con una sola query
SELECT tseq.executionTime, simbio_tcdetail.value  FROM simbio_tcseq  AS  tseq JOIN simbio_tcdetail  ON tseq.id = simbio_tcdetail.sec_id  WHERE 
    tseq.tcName_id = (SELECT stc.id FROM simbio_telecommand  stc  WHERE stc.tcDescription LIKE "%VIHI%" AND stc.tcDescription LIKE "%science%") 
    AND tseq.executionTime > "2018-12-11" AND tseq.executionTime < "2018-12-12"  AND simbio_tcdetail.parName_id = (SELECT tcp.id FROM simbio_tcparameter AS tcp 
    WHERE tcp.parDescription LIKE "%VIHI%" AND tcp.parDescription LIKE "%integration%")  ORDER BY tseq.executionTime LIMIT 1;