MAKE=make
FILE_TYPES= *.svg *.png *.jpg *.eps

all: rssi counter tx-problems duty-cycle ctp density counter-duty-cycle ctp-topology


density:
	./digraph_rssi.py data_rssi_cc2420_rssi_ch26_p__.py cc2420_conf.py "Indriya CH26 TXPower"


rssi:
	./graph_rssi.py data_rssi_cc2420_rssi_ch26_p__.py cc2420_conf.py "Indriya CC2420 RSSI CH26"
	#./graph_rssi.py data_rssi_rf212_rssi_ch0_p__.py rf212_conf.py "Twonet RF212 RSSI CH0"
	#./graph_rssi.py data_rssi_rf231_rssi_ch26_p__.py rf231_conf.py "Twonet RF231 RSSI CH26"


counter:
	./graph_counter.py data_counter_cc2420_counter_ch26_lpl0_r72_d60_p__.py cc2420_conf.py "Indriya CC2420 Counter CH26 LPL=0 Root=72 60sec" 1
	./graph_counter.py data_counter_cc2420_counter_ch26_lpl200_r72_d60_p__.py cc2420_conf.py "Indriya CC2420 Counter CH26 LPL=200 Root=72 60sec" 1
	./graph_counter.py data_counter_cc2420_counter_ch26_lpl200_r21_d60_p__.py cc2420_conf.py "Indriya CC2420 Counter CH26 LPL=200 Root=21 60sec" 1
	./graph_counter.py data_counter_cc2420_counter_ch26_lpl200_r21_d180_p__.py cc2420_conf.py "Indriya CC2420 Counter CH26 LPL=200 Root=21 180sec" 1
	#./graph_counter.py data_counter_rf212_counter_ch0_lpl0_r72_d60_p__.py rf212_conf.py "Twonet RF212 Counter CH0 LPL=0" 1
	#./graph_counter.py data_counter_rf231_counter_ch26_lpl0_r72_d60_p__.py rf231_conf.py "Twonet RF231 Counter CH26 LPL=0" 1


tx-problems:
	./graph_tx_problem.py data_tx_problem_cc2420_counter_ch26_lpl0_r72_d60_p__.py cc2420_conf.py "Indriya CC2420 TX Problems CH26 Root=72 60sec" 1
	#./graph_tx_problem.py data_tx_problem_rf212_counter_ch0_lpl0_r72_d60_p__.py rf212_conf.py "Twonet RF212 TX Problems CH0" 1
	#./graph_tx_problem.py data_tx_problem_rf231_counter_ch26_lpl0_r72_d60_p__.py rf231_conf.py "Twonet RF231 TX Problems CH26" 1 

duty-cycle:
	./graph_duty_cycle.py data_duty_cycle_cc2420_counter_ch26_lpl200_r72_d60_p__.py cc2420_conf.py "Indriya CC2420 Duty Cycle CH26 Root=72 60sec" 1
	./graph_duty_cycle.py data_duty_cycle_cc2420_counter_ch26_lpl200_r21_d60_p__.py cc2420_conf.py "Indriya CC2420 Duty Cycle CH26 Root=21 60sec" 1
	./graph_duty_cycle.py data_duty_cycle_cc2420_counter_ch26_lpl200_r21_d180_p__.py cc2420_conf.py "Indriya CC2420 Duty Cycle CH26 Root=21 180sec" 1
	#./graph_duty_cycle.py data_duty_cycle_rf212_counter_ch0_lpl200_r72_d60_p__.py rf212_conf.py "Twonet RF212 Duty Cycle CH0" 1
	#./graph_duty_cycle.py data_duty_cycle_rf231_counter_ch26_lpl200_r72_d60_p__.py rf231_conf.py "Twonet RF231 Duty Cycle CH26" 1 

counter-duty-cycle:
	./graph_counter_duty_cycle.py data_counter_cc2420_counter_ch26_lpl200_r72_d60_p__.py \
			data_duty_cycle_cc2420_counter_ch26_lpl200_r72_d60_p__.py cc2420_conf.py \
			"Indriya CC2420 Counter Duty Cycle CH26 Root=72 60sec" 1
	./graph_counter_duty_cycle.py data_counter_cc2420_counter_ch26_lpl200_r21_d60_p__.py \
			data_duty_cycle_cc2420_counter_ch26_lpl200_r21_d60_p__.py cc2420_conf.py \
			"Indriya CC2420 Counter Duty Cycle CH26 Root=21 60sec" 1
	./graph_counter_duty_cycle.py data_counter_cc2420_counter_ch26_lpl200_r21_d180_p__.py \
			data_duty_cycle_cc2420_counter_ch26_lpl200_r21_d180_p__.py cc2420_conf.py \
			"Indriya CC2420 Counter Duty Cycle CH26 Root=21 180sec" 1
	#./graph_counter_duty_cycle.py data_counter_rf212_counter_ch0_lpl0_r72_d60_p__.py data_duty_cycle_rf212_counter_ch0_lpl200_r72_d60_p__.py rf212_conf.py "Twonet RF212 Duty Cycle CH0" 1
	#./graph_counter_duty_cycle.py data_counter_rf231_counter_ch26_lpl0_r72_d60_p__.py data_duty_cycle_rf231_counter_ch26_lpl200_r72_d60_p__.py rf231_conf.py "Twonet RF231 Duty Cycle CH26" 1 

ctp:
	./graph_ctp_changes.py data_ctp_routing_cc2420_counter_ch26_lpl0_r72_d60_p__.py cc2420_conf.py "Indriya CC2420 CTP Routing CH26 LPL=0 Root=72 60sec" 1
	./graph_ctp_changes.py data_ctp_routing_cc2420_counter_ch26_lpl200_r72_d60_p__.py cc2420_conf.py "Indriya CC2420 CTP Routing CH26 LPL=200 Root=72 60sec" 1
	./graph_ctp_changes.py data_ctp_routing_cc2420_counter_ch26_lpl200_r21_d60_p__.py cc2420_conf.py "Indriya CC2420 CTP Routing CH26 LPL=200 Root=21 60sec" 1
	./graph_ctp_changes.py data_ctp_routing_cc2420_counter_ch26_lpl200_r21_d180_p__.py cc2420_conf.py "Indriya CC2420 CTP Routing CH26 LPL=200 Root=21 180sec" 1
	#./graph_ctp_changes.py data_ctp_routing_rf212_counter_ch0_lpl0_r72_d60_p__.py rf212_conf.py "Twonet RF212 CTP Routing CH0 LPL=0" 1
	#./graph_ctp_changes.py data_ctp_routing_rf231_counter_ch26_lpl0_r72_d60_p__.py rf231_conf.py "Twonet RF231 CTP Routing CH26 LPL=0" 1


ctp-topology:
	./digraph_topology.py data_ctp_routing_cc2420_counter_ch26_lpl0_r72_d60_p__.py cc2420_conf.py "Indriya CC2420 CTP Topology CH26 LPL=0 Root=72 60sec"
	./digraph_topology.py data_ctp_routing_cc2420_counter_ch26_lpl200_r72_d60_p__.py cc2420_conf.py "Indriya CC2420 CTP Topology CH26 LPL=200 Root=72 60sec"
	./digraph_topology.py data_ctp_routing_cc2420_counter_ch26_lpl200_r21_d60_p__.py cc2420_conf.py "Indriya CC2420 CTP Topology CH26 LPL=200 Root=21 60sec"
	./digraph_topology.py data_ctp_routing_cc2420_counter_ch26_lpl200_r21_d180_p__.py cc2420_conf.py "Indriya CC2420 CTP Topology CH26 LPL=200 Root=21 180sec"
	#./graph_ctp_changes.py data_ctp_routing_rf212_counter_ch0_lpl0_r72_d60_p__.py rf212_conf.py "Twonet RF212 CTP Routing CH0 LPL=0" 1
	#./graph_ctp_changes.py data_ctp_routing_rf231_counter_ch26_lpl0_r72_d60_p__.py rf231_conf.py "Twonet RF231 CTP Routing CH26 LPL=0" 1


leave-pdf:
	for f in $(FILE_TYPES); do rm $$f; done


clean: leave-pdf
	if [ -f *.pdf ]; then rm *.pdf; fi
