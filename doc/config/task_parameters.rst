Task Parameters
===============

The Task Parameters section contains details about
your task.  An example looks like this:

::

	[Task Parameters]
	experiment_code_version = 1.0
	num_conds = 1
	num_counters = 1
	allow_repeats = false
	always_show_instructions = true

`experiment_code_version`  [ string ]
-----------------------------------
Often you might a couple different versions
of an experiment during a research project (e.g.,
Experiment 1 and 2 of a papper).  
`experiment_code_version` is a string which is written into
the database along with your data helping you remember which
version of the code each participant was given.


`num_cond`  [ integer ]
---------------------
**psiTurk** includes a primitive system for counterbalancing
participants to conditions.  If you specify a number of
condition greater than 1, then **psiTurk** will attempt to
assign new participants to conditions to keep them all
with equal N.  It also takes into account the time delay
between a person being assigned to a condition and completing
a condition (or possibly withdrawing).  Thus, you can be
fairly assured that after running 100 subjects in two conditions
each condition will have 50+/- completed participants.

`num_counters`  [ integer ]
-------------------------
`num_counters` is identical to `num_cond` but provides
an additional counterbalancing factor beyond condition.
If `num_counters` is greater than 1 then **psiTurk**
behaves as if there are `num_cond*num_counters` conditions
and assigns subjects randomly to the the expanded design.
See `Issue #53 <https://github.com/NYUCCL/psiTurk/issues/53>`__
for more info.

`allow_repeats` [ true | false]
-----------------------------------------

If set to `true`, psiturk will not block a worker who has
already done the task (as assessed in the current database table).
This is to enable HITs where a worker might do a optional 
length sequence of smaller tasks rather than one long experiment.

`always_show_instructions` [ true | false]
-----------------------------------------

If set to `true`, psiturk will also present a worker with 
instructions, even if they have already completed the task.
If set to false, if the worker has already done the task or
HIT once (as assess in the current database table), then the
instructions will not be displayed again.  **Important** this
has to actually be implemented by the experimenter.  This just
provides a flag where you can check if you should show the
instructions again in your javascript code.
